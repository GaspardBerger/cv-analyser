#!/usr/bin/env python3
"""Upload-widget: bestandsupload + validatie voor de CV-analysator."""

import re

import streamlit as st

from translations import t

TOEGESTANE_TYPES = ["pdf", "docx"]
MAX_GROOTTE_MB = 10


def toon_upload_widget() -> object | None:
    """
    Toon de bestandsupload-widget en valideer het geüploade bestand.
    Geeft het UploadedFile-object terug, of None als er niets geldig is geüpload.
    """
    st.markdown(t("upload_header"))
    st.caption(t("upload_caption"))

    bestand = st.file_uploader(
        label=t("upload_label"),
        type=TOEGESTANE_TYPES,
        label_visibility="collapsed",
        help=t("upload_help"),
    )

    if bestand is None:
        return None

    # Grootte controleren
    grootte_mb = len(bestand.getbuffer()) / (1024 * 1024)
    if grootte_mb > MAX_GROOTTE_MB:
        st.error(t("upload_error_size", size=grootte_mb, max=MAX_GROOTTE_MB))
        return None

    naam = bestand.name
    extensie = naam.rsplit(".", 1)[-1].lower() if "." in naam else ""
    if extensie not in TOEGESTANE_TYPES:
        st.error(t("upload_error_type", ext=extensie))
        return None

    st.success(t("upload_success", name=naam, size=grootte_mb))

    # Bestandsnaam controleren op aanbevolen formaat: Cv_Voornaam Naam
    naam_zonder_ext = naam.rsplit(".", 1)[0] if "." in naam else naam
    if not re.match(r'^[Cc][Vv]_\S+', naam_zonder_ext):
        st.info(t("upload_filename_tip"))

    return bestand
