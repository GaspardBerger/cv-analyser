#!/usr/bin/env python3
"""Technische inspectie van een geüpload CV.

Wat hier gemeten wordt, hoeft de AI niet te gokken:

- pdf_metadata()    aantal pagina's, lettergroottes, lettertypes en uitlijning
- verborgen_tekst() tekst die onzichtbaar op de pagina staat (witte letters op
                    een witte achtergrond, of een piepklein lettertype) — de
                    klassieke drager van een prompt injection
- haal_foto()       de pasfoto uit het CV halen
- beoordeel_foto()  die foto laten beoordelen door Claude Vision

Alles is defensief geschreven: mislukt een meting, dan geeft de functie een
lege waarde terug en werkt de analyse gewoon verder zonder die gegevens.
"""

import base64
import json
import os
import re

# Tekst lichter dan deze drempel op een witte pagina beschouwen we als onzichtbaar
_WIT_DREMPEL = 0.92
# Lettergroottes hieronder zijn met het blote oog niet leesbaar
_MINI_LETTER_PT = 3.0
# Grenzen waarbinnen een afbeelding op een pasfoto lijkt
_FOTO_MIN_PX = 80
_FOTO_MAX_VERHOUDING = 1.6
_FOTO_MIN_VERHOUDING = 0.45


def _open_pdf(pdf_bytes: bytes):
    """Open een PDF uit bytes; geeft None terug als dat niet lukt."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return None
    try:
        return fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception:
        return None


def _kleur_helderheid(kleur_int: int) -> float:
    """Relatieve helderheid (0 = zwart, 1 = wit) van een sRGB-kleur."""
    r = ((kleur_int >> 16) & 255) / 255.0
    g = ((kleur_int >> 8) & 255) / 255.0
    b = (kleur_int & 255) / 255.0
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _is_onzichtbaar(span: dict) -> bool:
    """Staat deze tekst onzichtbaar op de pagina (wit of onleesbaar klein)?"""
    return (
        _kleur_helderheid(span.get("color", 0)) >= _WIT_DREMPEL
        or span.get("size", 99) < _MINI_LETTER_PT
    )


# ── Technische gegevens voor de lay-outcriteria ──────────────────────────────

def pdf_metadata(pdf_bytes: bytes) -> str:
    """Meet pagina's, lettergroottes, lettertypes en uitlijning van een PDF.

    Geeft een leesbare tekst terug voor de analyseprompt, of "" bij mislukking.
    """
    doc = _open_pdf(pdf_bytes)
    if doc is None:
        return ""

    try:
        groottes: dict[float, int] = {}
        lettertypes: set[str] = set()
        linkerranden: list[float] = []

        for pagina in doc:
            for blok in pagina.get_text("dict")["blocks"]:
                for lijn in blok.get("lines", []):
                    # Onzichtbare tekst mag de metingen niet vertekenen: anders
                    # zou een verstopte regel de "kleinste lettergrootte" bepalen
                    spans = [
                        s for s in lijn.get("spans", [])
                        if s.get("text", "").strip() and not _is_onzichtbaar(s)
                    ]
                    if not spans:
                        continue
                    # Linkerrand van elke tekstregel, voor de uitlijningscontrole
                    linkerranden.append(round(lijn["bbox"][0], 1))
                    for span in spans:
                        tekst = span["text"].strip()
                        grootte = round(span.get("size", 0), 1)
                        groottes[grootte] = groottes.get(grootte, 0) + len(tekst)
                        lettertypes.add(re.sub(r"^[A-Z]{6}\+", "", span.get("font", "")))

        if not groottes:
            return f"- Aantal pagina's: {len(doc)}"

        meest_gebruikt = max(groottes.items(), key=lambda kv: kv[1])[0]
        # Groottes met minder dan 20 tekens zijn paginanummers of voetnoten
        relevante = [g for g, n in groottes.items() if n >= 20] or list(groottes)

        regels = [
            f"- Aantal pagina's: {len(doc)}",
            f"- Kleinste lettergrootte (hoofdtekst): {min(relevante)}pt",
            f"- Meest gebruikte lettergrootte: {meest_gebruikt}pt",
            f"- Gebruikte lettertypes: {', '.join(sorted(lettertypes))}",
        ]
        uitlijning = _uitlijning_tekst(linkerranden)
        if uitlijning:
            regels.append(uitlijning)
        return "\n".join(regels)
    except Exception:
        return ""


def _uitlijning_tekst(linkerranden: list[float]) -> str:
    """Vat de linkeruitlijning samen: welke marges worden gebruikt en hoeveel
    regels vallen buiten de gangbare kolommen."""
    if len(linkerranden) < 5:
        return ""

    # Randen die binnen 2pt van elkaar liggen horen bij dezelfde kolom
    tellingen: dict[float, int] = {}
    for rand in linkerranden:
        for bestaande in tellingen:
            if abs(bestaande - rand) <= 2.0:
                tellingen[bestaande] += 1
                break
        else:
            tellingen[rand] = 1

    gesorteerd = sorted(tellingen.items(), key=lambda kv: -kv[1])
    hoofdkolommen = [(r, n) for r, n in gesorteerd if n >= 3]
    losse_regels = sum(n for r, n in gesorteerd if n < 3)

    kolom_tekst = ", ".join(f"{r:.0f}pt ({n} regels)" for r, n in hoofdkolommen[:5])
    return (
        f"- Uitlijning: linkermarges in gebruik: {kolom_tekst}; "
        f"{losse_regels} regel(s) beginnen op een afwijkende positie "
        f"(totaal {len(linkerranden)} regels)"
    )


# ── Verborgen tekst (mogelijke prompt injection) ─────────────────────────────

def verborgen_tekst(pdf_bytes: bytes) -> list[str]:
    """Zoek tekst die op de pagina onzichtbaar is.

    Twee gevallen: letters in (bijna) dezelfde kleur als de witte achtergrond,
    en letters die zo klein zijn dat ze niet te lezen zijn.
    """
    doc = _open_pdf(pdf_bytes)
    if doc is None:
        return []

    gevonden: list[str] = []
    try:
        for pagina in doc:
            for blok in pagina.get_text("dict")["blocks"]:
                for lijn in blok.get("lines", []):
                    for span in lijn.get("spans", []):
                        tekst = span.get("text", "").strip()
                        if len(tekst) < 12:
                            continue
                        if _is_onzichtbaar(span):
                            gevonden.append(tekst)
    except Exception:
        return []

    # Ontdubbelen met behoud van volgorde
    uniek: list[str] = []
    for tekst in gevonden:
        if tekst not in uniek:
            uniek.append(tekst)
    return uniek[:20]


# ── Pasfoto ──────────────────────────────────────────────────────────────────

def haal_foto(pdf_bytes: bytes) -> bytes | None:
    """Haal de meest waarschijnlijke pasfoto uit een CV-PDF (als PNG-bytes)."""
    doc = _open_pdf(pdf_bytes)
    if doc is None:
        return None

    try:
        import fitz

        kandidaten = []
        for pagina in doc:
            for info in pagina.get_images(full=True):
                xref = info[0]
                try:
                    pix = fitz.Pixmap(doc, xref)
                except Exception:
                    continue
                if pix.width < _FOTO_MIN_PX or pix.height < _FOTO_MIN_PX:
                    continue
                verhouding = pix.width / pix.height
                if not (_FOTO_MIN_VERHOUDING <= verhouding <= _FOTO_MAX_VERHOUDING):
                    continue
                # Een afbeelding die zowat de hele pagina beslaat is een
                # achtergrond of een gescande pagina, geen pasfoto
                if pix.width * pix.height > 4_000_000:
                    continue
                kandidaten.append(pix)

        if not kandidaten:
            return None

        # De grootste passende afbeelding is doorgaans de pasfoto
        beste = max(kandidaten, key=lambda p: p.width * p.height)
        if beste.n > 4 or beste.alpha:  # CMYK of alpha → omzetten naar RGB
            beste = fitz.Pixmap(fitz.csRGB, beste)
        return beste.tobytes("png")
    except Exception:
        return None


def beoordeel_foto(foto_bytes: bytes) -> dict:
    """Laat de pasfoto beoordelen door Claude Vision.

    Geeft een dict met de bevindingen, of {} als de beoordeling niet lukt.
    """
    try:
        import anthropic
    except ImportError:
        return {}

    api_sleutel = os.environ.get("ANTHROPIC_API_KEY")
    if not api_sleutel:
        return {}

    vraag = (
        "Dit is de foto uit een CV van een jongere die solliciteert. "
        "Beoordeel enkel de geschiktheid als CV-foto. Antwoord met JSON:\n"
        '{"persoon_zichtbaar": true, "portretfoto": true, "filter_of_effect": false, '
        '"professionele_houding": true, "neutrale_achtergrond": true, '
        '"geschikt": true, "opmerking": "één korte zin"}\n'
        "Let op filters of snapchat-effecten, zonnebril of pet, een vakantie- of "
        "feestcontext, een onverzorgde of te informele uitstraling, en of de "
        "achtergrond rustig is. Geef geen oordeel over uiterlijk, etniciteit, "
        "geslacht, leeftijd of aantrekkelijkheid — enkel over de professionele "
        "geschiktheid van de foto als zakelijk portret."
    )

    try:
        client = anthropic.Anthropic(api_key=api_sleutel)
        bericht = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=400,
            temperature=0.0,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": base64.standard_b64encode(foto_bytes).decode(),
                        },
                    },
                    {"type": "text", "text": vraag},
                ],
            }],
        )
        ruwe = bericht.content[0].text.strip()
        ruwe = re.sub(r"^```(?:json)?\s*|\s*```$", "", ruwe)
        return json.loads(ruwe)
    except Exception:
        return {}


def foto_tekst(beoordeling: dict) -> str:
    """Zet de fotobeoordeling om naar een regel voor de analyseprompt."""
    if not beoordeling:
        return ""
    def ja_nee(sleutel: str) -> str:
        waarde = beoordeling.get(sleutel)
        return "ja" if waarde is True else "nee" if waarde is False else "onbekend"

    return (
        "- Fotobeoordeling (automatisch): "
        f"persoon zichtbaar: {ja_nee('persoon_zichtbaar')}; "
        f"portretfoto: {ja_nee('portretfoto')}; "
        f"filter of effect: {ja_nee('filter_of_effect')}; "
        f"professionele houding: {ja_nee('professionele_houding')}; "
        f"neutrale achtergrond: {ja_nee('neutrale_achtergrond')}; "
        f"geschikt als CV-foto: {ja_nee('geschikt')}"
        + (f"; opmerking: {beoordeling['opmerking']}" if beoordeling.get("opmerking") else "")
    )
