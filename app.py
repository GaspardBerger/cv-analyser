#!/usr/bin/env python3
"""CV-Analysator — Gluon Educatie. Streamlit hoofdapplicatie."""

import os
import sys

import streamlit as st
from dotenv import load_dotenv

# Lokaal: laad .env bestand
load_dotenv()

# Streamlit Cloud: haal API-sleutel uit st.secrets en zet in os.environ
try:
    if "ANTHROPIC_API_KEY" in st.secrets:
        os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    pass

# Zorg dat de projectmap in het Python-pad zit
sys.path.insert(0, os.path.dirname(__file__))

from core.analyzer import analyseer_cv
from core.extractor import extraheer_tekst
from core.privacy import tijdelijk_bestand
from translations import LANGUAGE_OPTIONS, t
from ui.criteria_editor import toon_criteria_editor
from ui.results import toon_resultaten
from ui.upload import toon_upload_widget


st.set_page_config(
    page_title="CV Analyser — Gluon Educatie",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Sessie-state initialiseren
if "analyse_resultaat" not in st.session_state:
    st.session_state.analyse_resultaat = None
if "criteria_override" not in st.session_state:
    st.session_state.criteria_override = None
if "lang" not in st.session_state:
    st.session_state["lang"] = "nl"

# Language selector (small, top right)
_lang_options = list(LANGUAGE_OPTIONS.keys())
_lang_reverse = {v: k for k, v in LANGUAGE_OPTIONS.items()}
_, _lang_col = st.columns([5, 1])
with _lang_col:
    _selected = st.selectbox(
        "Language",
        options=_lang_options,
        index=_lang_options.index(_lang_reverse.get(st.session_state["lang"], "Nederlands")),
        label_visibility="collapsed",
    )
st.session_state["lang"] = LANGUAGE_OPTIONS[_selected]


def _controleer_api_sleutel() -> bool:
    sleutel = os.environ.get("ANTHROPIC_API_KEY", "")
    if not sleutel or not sleutel.startswith("sk-"):
        st.error(t("api_key_error"))
        return False
    return True


def _nieuwe_analyse():
    st.session_state.analyse_resultaat = None
    st.rerun()


# Header
st.markdown(f"# {t('app_header')}")
st.markdown(t("app_subtitle"))
st.divider()

# API-sleutel controleren
if not _controleer_api_sleutel():
    st.stop()

# Toon resultaten als analyse al gedaan is
if st.session_state.analyse_resultaat is not None:
    toon_resultaten(st.session_state.analyse_resultaat)
    st.divider()
    if st.button(t("btn_new_analysis"), type="secondary"):
        _nieuwe_analyse()
    st.stop()

# Upload-widget
bestand = toon_upload_widget()

# Criteria-editor voor begeleiders
criteria_override = toon_criteria_editor()

# Analyseknop
if bestand is not None:
    st.divider()
    if st.button(t("btn_analyse"), type="primary", use_container_width=True):
        extensie = "." + bestand.name.rsplit(".", 1)[-1].lower()

        with st.spinner(t("spinner")):
            # Stap 1: tekst extraheren (tijdelijk bestand, direct verwijderd)
            with tijdelijk_bestand(bestand, extensie) as pad:
                tekst, waarschuwing = extraheer_tekst(pad)

            if waarschuwing:
                st.warning(waarschuwing)
                st.stop()

            if not tekst:
                st.error(t("error_no_text"))
                st.stop()

            # Stap 2: analyse via Claude API
            try:
                resultaat = analyseer_cv(
                    tekst,
                    criteria_override=criteria_override,
                    lang=st.session_state["lang"],
                )
            except RuntimeError as fout:
                st.error(str(fout))
                st.stop()
            except Exception as fout:
                fout_str = str(fout).lower()
                if "connection" in fout_str or "network" in fout_str or "timeout" in fout_str:
                    st.error(t("error_no_connection"))
                else:
                    st.error(t("error_unexpected", error=fout))
                st.stop()

        st.session_state.analyse_resultaat = resultaat
        st.rerun()

# Voettekst
st.divider()
st.caption(t("footer"))
