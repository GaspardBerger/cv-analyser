#!/usr/bin/env python3
"""CV-preview met foutmarkeringen.

- PDF: pagina's worden gerenderd als afbeeldingen; per verbeterpunt met een
  "citaat" wordt dat tekstfragment opgezocht en gemarkeerd met een rood
  stippellijnkader plus een genummerd bolletje dat overeenkomt met het
  nummer van het verbeterpunt in de linkerkolom.
- DOCX: geen paginaweergave mogelijk; de uitgeleste tekst wordt getoond als
  HTML waarin de citaten met een stippellijnkader gemarkeerd zijn.

Ook: pdf_metadata() meet aantal pagina's, lettergroottes en lettertypes,
zodat de lay-outcriteria (lengte, leesbaarheid, consequent lettertype)
objectief beoordeeld kunnen worden.
"""

import html
import re

_ROOD = (0.91, 0.30, 0.24)  # #e74c3c, zelfde rood als de UI


# ── PDF-metadata voor de lay-outcriteria ─────────────────────────────────────

def pdf_metadata(pdf_bytes: bytes) -> str:
    """Meet aantal pagina's, lettergroottes en lettertypes van een PDF.

    Geeft een leesbare tekst terug voor de analyseprompt, of "" bij mislukking.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return ""

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        groottes: dict[float, int] = {}
        lettertypes: set[str] = set()

        for pagina in doc:
            for blok in pagina.get_text("dict")["blocks"]:
                for lijn in blok.get("lines", []):
                    for span in lijn.get("spans", []):
                        tekst = span.get("text", "").strip()
                        if not tekst:
                            continue
                        grootte = round(span.get("size", 0), 1)
                        groottes[grootte] = groottes.get(grootte, 0) + len(tekst)
                        lettertypes.add(re.sub(r"^[A-Z]{6}\+", "", span.get("font", "")))

        if not groottes:
            return f"- Aantal pagina's: {len(doc)}"

        meest_gebruikt = max(groottes.items(), key=lambda kv: kv[1])[0]
        # Negeer groottes met minder dan 20 tekens (paginanummers, voetnoten)
        relevante = [g for g, n in groottes.items() if n >= 20] or list(groottes)
        return (
            f"- Aantal pagina's: {len(doc)}\n"
            f"- Kleinste lettergrootte (hoofdtekst): {min(relevante)}pt\n"
            f"- Meest gebruikte lettergrootte: {meest_gebruikt}pt\n"
            f"- Gebruikte lettertypes: {', '.join(sorted(lettertypes))}"
        )
    except Exception:
        return ""


# ── PDF-preview met markeringen ──────────────────────────────────────────────

def render_pdf_met_markeringen(
    pdf_bytes: bytes, verbeterpunten: list[dict]
) -> tuple[list[bytes], set[int]]:
    """Render PDF-pagina's als PNG's met stippellijnkaders rond de citaten.

    Geeft terug: (lijst met PNG-bytes per pagina, set met prioriteitsnummers
    die effectief op het CV gemarkeerd konden worden).
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return [], set()

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception:
        return [], set()

    gemarkeerd: set[int] = set()

    for punt in verbeterpunten:
        citaat = (punt.get("citaat") or "").strip()
        if not citaat:
            continue
        nummer = punt.get("prioriteit", 0)

        for pagina in doc:
            rects = _zoek_citaat(pagina, citaat)
            if not rects:
                continue
            # Eén kader rond alle lijnen van dezelfde vindplaats
            kader = rects[0]
            for r in rects[1:]:
                kader |= r
            kader = fitz.Rect(kader.x0 - 4, kader.y0 - 3, kader.x1 + 4, kader.y1 + 3)
            pagina.draw_rect(kader, color=_ROOD, width=1.5, dashes="[4 3] 0")

            # Genummerd bolletje op de linkerbovenhoek van het kader (als speldje)
            straal = 8.0
            cx = max(straal + 2, kader.x0)
            cy = max(straal + 2, kader.y0)
            pagina.draw_circle(fitz.Point(cx, cy), straal, color=_ROOD, fill=_ROOD)
            pagina.insert_text(
                fitz.Point(cx - 2.8, cy + 3.4),
                str(nummer),
                fontsize=10,
                color=(1, 1, 1),
            )
            gemarkeerd.add(nummer)
            break

    afbeeldingen = []
    try:
        for pagina in doc:
            pix = pagina.get_pixmap(matrix=fitz.Matrix(2, 2))
            afbeeldingen.append(pix.tobytes("png"))
    except Exception:
        return [], set()

    return afbeeldingen, gemarkeerd


def _zoek_citaat(pagina, citaat: str) -> list:
    """Zoek een citaat op een pagina; probeer steeds kortere varianten."""
    rects = pagina.search_for(citaat)
    if rects:
        return _eerste_vindplaats(rects)

    woorden = citaat.split()
    for aantal in (6, 4, 3):
        if len(woorden) > aantal:
            rects = pagina.search_for(" ".join(woorden[:aantal]))
            if rects:
                return _eerste_vindplaats(rects)
    return []


def _eerste_vindplaats(rects: list) -> list:
    """Beperk de zoekresultaten tot de eerste vindplaats (aaneensluitende lijnen)."""
    eerste = [rects[0]]
    for r in rects[1:]:
        # Lijnen van dezelfde vindplaats sluiten verticaal op elkaar aan
        if 0 <= r.y0 - eerste[-1].y1 <= 6:
            eerste.append(r)
        else:
            break
    return eerste


# ── DOCX-fallback: tekstpreview met markeringen ──────────────────────────────

def tekst_preview_html(cv_tekst: str, verbeterpunten: list[dict]) -> tuple[str, set[int]]:
    """Bouw een HTML-preview van de uitgeleste tekst met gemarkeerde citaten.

    Geeft terug: (HTML-string, set met prioriteitsnummers die gemarkeerd zijn).
    """
    gemarkeerd: set[int] = set()
    veilig = html.escape(cv_tekst)

    # Langste citaten eerst, zodat kortere citaten geen deel van een al
    # geplaatste markering vervangen
    punten = sorted(
        (p for p in verbeterpunten if (p.get("citaat") or "").strip()),
        key=lambda p: -len(p["citaat"]),
    )
    for punt in punten:
        citaat = html.escape(punt["citaat"].strip())
        nummer = punt.get("prioriteit", 0)
        if citaat not in veilig:
            continue
        badge = (
            f'<sup style="background:#e74c3c;color:#fff;border-radius:50%;'
            f'padding:1px 5px;font-size:11px;font-weight:bold;">{nummer}</sup>'
        )
        markering = (
            f'<span style="border:2px dashed #e74c3c;border-radius:4px;'
            f'padding:0 3px;">{citaat}</span>{badge}'
        )
        veilig = veilig.replace(citaat, markering, 1)
        gemarkeerd.add(nummer)

    html_blok = (
        '<div style="background:#fff;color:#222;border:1px solid #ddd;'
        'border-radius:8px;padding:24px;max-height:900px;overflow-y:auto;'
        'white-space:pre-wrap;font-family:Georgia,serif;font-size:14px;'
        f'line-height:1.5;">{veilig}</div>'
    )
    return html_blok, gemarkeerd
