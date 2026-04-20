#!/usr/bin/env python3
"""Claude API-integratie voor CV-analyse: laadt criteria en geeft een gestructureerd JSON-rapport."""

import json
import os
import re
from pathlib import Path

import yaml


CRITERIA_PAD = Path(__file__).parent.parent / "config" / "criteria.yaml"

SCORE_LABELS = {
    (0, 40): "Vereist veel werk",
    (41, 59): "Voldoende",
    (60, 74): "Goed",
    (75, 89): "Zeer goed",
    (90, 100): "Uitstekend",
}


def _score_label(score: int) -> str:
    for (laag, hoog), label in SCORE_LABELS.items():
        if laag <= score <= hoog:
            return label
    return "Onbekend"


def laad_criteria(criteria_override: dict | None = None) -> dict:
    """Laad criteria uit YAML of gebruik een overschreven versie vanuit de UI."""
    if criteria_override:
        return criteria_override
    with open(CRITERIA_PAD, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _bouw_criteria_tekst(criteria_data: dict) -> str:
    """Zet criteria-YAML om naar een genummerde tekst voor de prompt."""
    regels = []
    teller = 1
    for cat_id, cat in criteria_data["categorieen"].items():
        regels.append(f"\n## {cat['naam']} (gewicht: {cat['gewicht']}%)")
        for c in cat["criteria"]:
            verplicht = "VERPLICHT" if c.get("verplicht") else "optioneel"
            regels.append(f"{teller}. [{verplicht}] {c['beschrijving']} (gewicht: {c['gewicht']} punten, id: {c['id']})")
            teller += 1
    return "\n".join(regels)


def _bouw_system_prompt(criteria_data: dict) -> str:
    criteria_tekst = _bouw_criteria_tekst(criteria_data)
    context = criteria_data.get("context", {})
    doelgroep = context.get("doelgroep", "jongeren op de arbeidsmarkt")
    taal_hint = context.get("taal_hint", "analyseer in de taal van het CV maar geef analyse in het Nederlands")

    return f"""Je bent een CV-expert voor de Belgische arbeidsmarkt, gespecialiseerd in het helpen van {doelgroep} bij het verbeteren van hun CV.

Je analyseert CV's aan de hand van specifieke criteria en geeft een score van 0–100 plus maximaal 5 concrete, bemoedigende verbeterpunten.

TAALINSTRUCTIE: {taal_hint}

CRITERIA VOOR BEOORDELING:
{criteria_tekst}

BEOORDELINGSWIJZE:
- Beoordeel elk criterium: 0 (niet aanwezig), 0.5 (gedeeltelijk aanwezig), of 1 (volledig aanwezig)
- Bereken een gewogen totaalscore van 0–100 op basis van de opgegeven gewichten
- Geef maximaal 5 verbeterpunten, gerangschikt van meest naar minst impactvol
- Elk verbeterpunt bevat: wat ontbreekt, waarom het belangrijk is, en een concreet voorbeeld
- Gebruik een bemoedigende en constructieve toon, geschikt voor jongeren die de arbeidsmarkt betreden
- Noem ook 2–3 sterke punten om de deelnemer te motiveren

VERPLICHT OUTPUT FORMAT — geef ENKEL dit JSON-object terug, zonder markdown, zonder uitleg erbuiten:
{{
  "totaalscore": 72,
  "score_label": "Goed",
  "categorie_scores": {{
    "structuur_opmaak": {{"score": 18, "max": 25, "label": "Goed"}},
    "inhoud": {{"score": 25, "max": 35, "label": "Uitstekend"}},
    "taal_schrijfstijl": {{"score": 20, "max": 25, "label": "Goed"}},
    "professionaliteit": {{"score": 9, "max": 15, "label": "Voldoende"}}
  }},
  "verbeterpunten": [
    {{
      "prioriteit": 1,
      "categorie": "taal_schrijfstijl",
      "titel": "Voeg meetbare prestaties toe",
      "probleem": "De werkervaring beschrijft taken maar geen resultaten.",
      "waarom": "Werkgevers willen zien wat je hebt bereikt, niet alleen wat je deed.",
      "voorbeeld": "In plaats van 'klantenservice gedaan', schrijf: '30+ klanten per dag geholpen, klanttevredenheid verhoogd met 15%%'.",
      "criterium_id": "meetbare_prestaties"
    }}
  ],
  "sterke_punten": [
    "Duidelijke contactgegevens met LinkedIn-profiel",
    "Goede talenkennis met CEFR-niveaus vermeld"
  ],
  "taal_cv": "nl",
  "samenvatting": "Dit CV toont een solide basis. Met enkele gerichte aanpassingen wordt het aanzienlijk sterker."
}}"""


def analyseer_cv(cv_tekst: str, criteria_override: dict | None = None) -> dict:
    """
    Analyseer een CV-tekst via de Claude API.

    Geeft terug: dict met score, verbeterpunten en sterke punten.
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
    system_prompt = _bouw_system_prompt(criteria_data)

    client = anthropic.Anthropic(api_key=api_sleutel)

    bericht = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"Analyseer dit CV:\n\n{cv_tekst}",
            }
        ],
    )

    ruwe_tekst = bericht.content[0].text.strip()
    return _parseer_json(ruwe_tekst)


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
