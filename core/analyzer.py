#!/usr/bin/env python3
"""Claude API-integratie voor CV-analyse.

De AI beoordeelt elk criterium afzonderlijk (0 / 0.5 / 1); de eindscore wordt
daarna deterministisch in Python berekend op basis van de gewichten in
criteria.yaml. Dezelfde beoordelingen leveren dus altijd exact dezelfde score
op, en elk criterium is zichtbaar in het resultaat (geen verborgen criteria).
"""

import json
import os
import re
from pathlib import Path

import yaml


CRITERIA_PAD = Path(__file__).parent.parent / "config" / "criteria.yaml"

# Internal English keys used in JSON output and UI color mapping
SCORE_LABELS = {
    (0, 40): "needs_work",
    (41, 59): "sufficient",
    (60, 74): "good",
    (75, 89): "very_good",
    (90, 100): "excellent",
}

_LANG_INSTRUCTIONS = {
    "nl": "geef de analyse in het Nederlands",
    "fr": "donne l'analyse en français",
    "en": "give the analysis in English",
}

MAX_VERBETERPUNTEN = 5


def _score_label(score: int) -> str:
    for (laag, hoog), label in SCORE_LABELS.items():
        if laag <= score <= hoog:
            return label
    return "unknown"


def laad_criteria(criteria_override: dict | None = None) -> dict:
    """Laad criteria uit YAML of gebruik een overschreven versie vanuit de UI."""
    if criteria_override:
        return criteria_override
    with open(CRITERIA_PAD, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _actieve_criteria(cat: dict) -> list[dict]:
    """Geef de actieve criteria van een categorie (editor kan criteria uitschakelen)."""
    return [c for c in cat.get("criteria", []) if c.get("actief", True)]


def _bouw_criteria_tekst(criteria_data: dict) -> str:
    """Zet criteria-YAML om naar een genummerde tekst voor de prompt."""
    regels = []
    teller = 1
    for cat_id, cat in criteria_data["categorieen"].items():
        actief = _actieve_criteria(cat)
        if not actief:
            continue
        regels.append(f"\n## {cat['naam']} (gewicht: {cat['gewicht']}%)")
        for c in actief:
            verplicht = "VERPLICHT" if c.get("verplicht") else "optioneel"
            regels.append(f"{teller}. [{verplicht}] {c['beschrijving']} (id: {c['id']})")
            teller += 1
    return "\n".join(regels)


def _alle_criterium_ids(criteria_data: dict) -> list[str]:
    ids = []
    for cat in criteria_data["categorieen"].values():
        ids.extend(c["id"] for c in _actieve_criteria(cat))
    return ids


def _bouw_system_prompt(criteria_data: dict, lang: str = "nl") -> str:
    criteria_tekst = _bouw_criteria_tekst(criteria_data)
    ids = ", ".join(_alle_criterium_ids(criteria_data))
    context = criteria_data.get("context", {})
    doelgroep = context.get("doelgroep", "jongeren op de arbeidsmarkt")
    taal_instructie = _LANG_INSTRUCTIONS.get(lang, _LANG_INSTRUCTIONS["nl"])

    return f"""Je bent een CV-expert voor de Belgische arbeidsmarkt, gespecialiseerd in het helpen van {doelgroep} bij het verbeteren van hun CV.

Je beoordeelt het CV criterium per criterium. Jij berekent GEEN totaalscore — dat gebeurt achteraf automatisch op basis van vaste gewichten.

TAALINSTRUCTIE: Het CV kan in NL, FR of EN zijn. {taal_instructie}.

CRITERIA VOOR BEOORDELING:
{criteria_tekst}

BEOORDELINGSWIJZE:
- Beoordeel ELK criterium met exact één van deze waarden: 0 (niet aanwezig), 0.5 (gedeeltelijk aanwezig), 1 (volledig aanwezig)
- Neem ELK criterium-id op in "criteria_beoordeling", zonder er over te slaan: {ids}
- Wees strikt consistent en objectief: baseer elk oordeel uitsluitend op wat letterlijk in de CV-tekst staat, niet op interpretatie of stijlvoorkeur. Hetzelfde CV moet altijd exact dezelfde beoordeling per criterium krijgen.
- Geef bij elk criterium een korte "toelichting" (één zin) die uitlegt waarom je 0, 0.5 of 1 gaf
- Geef bij elk criterium met score lager dan 1 ook: "titel" (korte actiegerichte titel), "probleem" (wat ontbreekt), "waarom" (waarom het belangrijk is) en "voorbeeld" (een concreet voorbeeld dat de deelnemer kan overnemen)
- Gebruik een bemoedigende en constructieve toon, geschikt voor jongeren die de arbeidsmarkt betreden
- Noem ook 2–3 sterke punten om de deelnemer te motiveren

ADRESCONTROLE:
- Zoek het adres (straat, nummer, gemeente) in het CV
- Controleer of het adres in dezelfde taal geschreven is als de rest van het CV. Let op: veel Brusselse en Belgische straatnamen en gemeenten hebben een Nederlandse én een Franse variant (bv. "Wetstraat" / "Rue de la Loi", "Elsene" / "Ixelles"). In een Nederlandstalig CV hoort de Nederlandse variant, in een Franstalig CV de Franse variant.
- Rapporteer het resultaat in "adres_check"

VERPLICHT OUTPUT FORMAT — geef ENKEL dit JSON-object terug, zonder markdown, zonder uitleg erbuiten:
{{
  "criteria_beoordeling": {{
    "contactgegevens": {{"score": 1, "toelichting": "..."}},
    "meetbare_prestaties": {{"score": 0, "toelichting": "...", "titel": "...", "probleem": "...", "waarom": "...", "voorbeeld": "..."}}
  }},
  "sterke_punten": ["...", "..."],
  "taal_cv": "nl",
  "adres_check": {{
    "adres_gevonden": true,
    "adres": "Wetstraat 16, 1000 Brussel",
    "taal_adres": "nl",
    "komt_overeen": true,
    "opmerking": "..."
  }},
  "samenvatting": "..."
}}"""


def _normaliseer_verdict(waarde) -> float:
    """Zet de score van de AI om naar exact 0, 0.5 of 1."""
    try:
        v = float(waarde)
    except (TypeError, ValueError):
        return 0.0
    if v < 0.25:
        return 0.0
    if v < 0.75:
        return 0.5
    return 1.0


def _bereken_resultaat(ruwe: dict, criteria_data: dict) -> dict:
    """Bereken de scores deterministisch in Python op basis van de vaste gewichten.

    De AI levert enkel de beoordeling per criterium (0 / 0.5 / 1); alle
    rekenwerk en de selectie/volgorde van verbeterpunten gebeurt hier, zodat
    dezelfde beoordelingen altijd hetzelfde rapport opleveren.
    """
    beoordelingen = ruwe.get("criteria_beoordeling", {})
    checklist = []
    categorie_scores = {}
    verbeter_kandidaten = []
    totaal_raw = 0.0
    volgorde = 0

    for cat_id, cat in criteria_data["categorieen"].items():
        actief = _actieve_criteria(cat)
        if not actief:
            continue
        cat_gewicht = cat["gewicht"]
        som_gewichten = sum(c["gewicht"] for c in actief) or 1
        behaald = 0.0

        for c in actief:
            volgorde += 1
            beoordeling = beoordelingen.get(c["id"], {})
            verdict = _normaliseer_verdict(beoordeling.get("score"))
            # Gewicht geschaald naar het categoriegewicht, zodat de totalen
            # ook kloppen wanneer een begeleider criteria uit- of aanzet
            gewicht = cat_gewicht * c["gewicht"] / som_gewichten
            behaald += gewicht * verdict

            checklist.append({
                "criterium_id": c["id"],
                "categorie": cat_id,
                "beschrijving": c["beschrijving"],
                "verplicht": bool(c.get("verplicht")),
                "score": verdict,
                "gewicht": round(gewicht, 1),
                "toelichting": beoordeling.get("toelichting", ""),
            })

            if verdict < 1.0:
                verbeter_kandidaten.append({
                    "impact": gewicht * (1.0 - verdict),
                    "volgorde": volgorde,
                    "categorie": cat_id,
                    "criterium_id": c["id"],
                    "titel": beoordeling.get("titel") or c["beschrijving"],
                    "probleem": beoordeling.get("probleem", ""),
                    "waarom": beoordeling.get("waarom", ""),
                    "voorbeeld": beoordeling.get("voorbeeld", ""),
                })

        totaal_raw += behaald
        cat_score = round(behaald)
        categorie_scores[cat_id] = {
            "score": cat_score,
            "max": cat_gewicht,
            "label": _score_label(round(behaald / cat_gewicht * 100)) if cat_gewicht else "unknown",
        }

    # Verbeterpunten: deterministisch gerangschikt op te winnen punten,
    # bij gelijke impact op volgorde in criteria.yaml
    verbeter_kandidaten.sort(key=lambda k: (-k["impact"], k["volgorde"]))
    verbeterpunten = []
    for i, kandidaat in enumerate(verbeter_kandidaten[:MAX_VERBETERPUNTEN], start=1):
        verbeterpunten.append({
            "prioriteit": i,
            "categorie": kandidaat["categorie"],
            "titel": kandidaat["titel"],
            "probleem": kandidaat["probleem"],
            "waarom": kandidaat["waarom"],
            "voorbeeld": kandidaat["voorbeeld"],
            "criterium_id": kandidaat["criterium_id"],
        })

    totaalscore = round(totaal_raw)
    return {
        "totaalscore": totaalscore,
        "score_label": _score_label(totaalscore),
        "categorie_scores": categorie_scores,
        "criteria_checklist": checklist,
        "verbeterpunten": verbeterpunten,
        "sterke_punten": ruwe.get("sterke_punten", []),
        "taal_cv": ruwe.get("taal_cv", ""),
        "adres_check": ruwe.get("adres_check", {}),
        "samenvatting": ruwe.get("samenvatting", ""),
    }


def analyseer_cv(cv_tekst: str, criteria_override: dict | None = None, lang: str = "nl") -> dict:
    """
    Analyseer een CV-tekst via de Claude API.

    Geeft terug: dict met score, volledige criteria-checklist, verbeterpunten,
    sterke punten en adrescontrole.
    Gooit een RuntimeError bij een onherstelbare fout.
    """
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("anthropic is niet geïnstalleerd. Voer 'pip install anthropic' uit.")

    api_sleutel = os.environ.get("ANTHROPIC_API_KEY")
    if not api_sleutel:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is niet ingesteld. "
            "Maak een .env bestand aan met ANTHROPIC_API_KEY=jouw-sleutel."
        )

    criteria_data = laad_criteria(criteria_override)
    system_prompt = _bouw_system_prompt(criteria_data, lang=lang)

    client = anthropic.Anthropic(api_key=api_sleutel)

    bericht = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        temperature=0.0,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"Analyseer dit CV:\n\n{cv_tekst}",
            }
        ],
    )

    ruwe_tekst = bericht.content[0].text.strip()
    ruwe = _parseer_json(ruwe_tekst)
    return _bereken_resultaat(ruwe, criteria_data)


def _parseer_json(tekst: str) -> dict:
    """Parseer JSON uit de Claude-respons, met een regex-fallback voor onverwacht omringende tekst."""
    try:
        return json.loads(tekst)
    except json.JSONDecodeError:
        pass

    # Fallback: zoek het eerste volledige JSON-object in de tekst
    match = re.search(r"\{.*\}", tekst, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise RuntimeError(
        "De analyse kon niet worden verwerkt. "
        "Probeer het opnieuw of controleer je internetverbinding."
    )
