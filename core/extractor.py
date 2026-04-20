#!/usr/bin/env python3
"""Tekstextractie uit PDF- en DOCX-bestanden voor CV-analyse."""

from pathlib import Path


def extraheer_tekst(bestandspad: str) -> tuple[str, str | None]:
    """
    Extraheer leesbare tekst uit een PDF of DOCX bestand.

    Geeft terug: (tekst, waarschuwing)
    - tekst: geëxtraheerde CV-tekst (leeg bij mislukking)
    - waarschuwing: melding als het bestand niet goed leesbaar is (anders None)
    """
    pad = Path(bestandspad)
    suffix = pad.suffix.lower()

    if suffix == ".pdf":
        return _extraheer_pdf(bestandspad)
    elif suffix in (".docx", ".doc"):
        return _extraheer_docx(bestandspad)
    else:
        return "", f"Bestandsformaat '{suffix}' wordt niet ondersteund. Gebruik PDF of DOCX."


def _extraheer_pdf(pad: str) -> tuple[str, str | None]:
    try:
        import pdfplumber
    except ImportError:
        return "", "pdfplumber is niet geïnstalleerd. Voer 'pip install pdfplumber' uit."

    tekst_delen = []
    try:
        with pdfplumber.open(pad) as pdf:
            for pagina in pdf.pages:
                inhoud = pagina.extract_text()
                if inhoud:
                    tekst_delen.append(inhoud)
    except Exception as fout:
        return "", f"Kon de PDF niet lezen: {fout}"

    tekst = "\n".join(tekst_delen).strip()

    if not tekst or len(tekst) < 50:
        return "", (
            "Er kon geen tekst worden uitgelezen uit dit PDF-bestand. "
            "Dit komt voor bij gescande of afbeelding-PDF's. "
            "Exporteer je CV als PDF vanuit Word of een tekstverwerkingsprogramma."
        )

    return tekst, None


def _extraheer_docx(pad: str) -> tuple[str, str | None]:
    try:
        from docx import Document
    except ImportError:
        return "", "python-docx is niet geïnstalleerd. Voer 'pip install python-docx' uit."

    try:
        doc = Document(pad)
    except Exception as fout:
        fout_str = str(fout).lower()
        if "encrypted" in fout_str or "password" in fout_str or "corrupt" in fout_str:
            return "", (
                "Dit Word-bestand is beveiligd met een wachtwoord of beschadigd. "
                "Sla het op als een nieuw bestand zonder wachtwoordbeveiliging."
            )
        return "", f"Kon het Word-bestand niet openen: {fout}"

    alineas = [p.text for p in doc.paragraphs if p.text.strip()]

    # Tekst in tabellen (veel CV's gebruiken tabellen voor lay-out)
    for tabel in doc.tables:
        for rij in tabel.rows:
            for cel in rij.cells:
                cel_tekst = cel.text.strip()
                if cel_tekst and cel_tekst not in alineas:
                    alineas.append(cel_tekst)

    tekst = "\n".join(alineas).strip()

    if not tekst or len(tekst) < 50:
        return "", "Het Word-bestand lijkt leeg of bevat alleen afbeeldingen."

    return tekst, None
