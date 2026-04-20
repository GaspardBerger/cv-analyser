#!/usr/bin/env python3
"""Upload-widget: bestandsupload + validatie voor de CV-analysator."""

import streamlit as st

TOEGESTANE_TYPES = ["pdf", "docx"]
MAX_GROOTTE_MB = 10


def toon_upload_widget() -> object | None:
    """
    Toon de bestandsupload-widget en valideer het geüploade bestand.
    Geeft het UploadedFile-object terug, of None als er niets geldig is geüpload.
    """
    st.markdown("### Jouw CV uploaden")
    st.caption("Ondersteunde formaten: PDF en Word (.docx) — maximaal 10 MB")

    bestand = st.file_uploader(
        label="Kies je CV",
        type=TOEGESTANE_TYPES,
        label_visibility="collapsed",
        help="Sleep je CV hierheen of klik om een bestand te kiezen.",
    )

    if bestand is None:
        return None

    # Grootte controleren
    grootte_mb = len(bestand.getbuffer()) / (1024 * 1024)
    if grootte_mb > MAX_GROOTTE_MB:
        st.error(
            f"Het bestand is te groot ({grootte_mb:.1f} MB). "
            f"Maximale bestandsgrootte is {MAX_GROOTTE_MB} MB."
        )
        return None

    naam = bestand.name
    extensie = naam.rsplit(".", 1)[-1].lower() if "." in naam else ""
    if extensie not in TOEGESTANE_TYPES:
        st.error(
            f"Bestandstype '.{extensie}' wordt niet ondersteund. "
            "Upload een PDF- of Word-bestand (.docx)."
        )
        return None

    st.success(f"Bestand geladen: **{naam}** ({grootte_mb:.2f} MB)")
    return bestand
