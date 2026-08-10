#!/usr/bin/env python3
"""CV-Analysator — Gluon Educatie. Streamlit hoofdapplicatie."""

import json
import os
import sys

import streamlit as st

# Lokaal: laad .env bestand (niet nodig op Streamlit Cloud)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

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
from core.preview import pdf_metadata
from core.privacy import tijdelijk_bestand
from translations import LANGUAGE_OPTIONS, t
from ui.criteria_editor import toon_criteria_editor
from ui.results import toon_resultaten
from ui.upload import toon_upload_widget


st.set_page_config(
    page_title="CV Analyser — Gluon Educatie",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Sessie-state initialiseren
if "analyse_resultaat" not in st.session_state:
    st.session_state.analyse_resultaat = None
if "criteria_override" not in st.session_state:
    st.session_state.criteria_override = None
if "lang" not in st.session_state:
    st.session_state["lang"] = "nl"
if "ocr_gebruikt" not in st.session_state:
    st.session_state.ocr_gebruikt = False
# Bestand + tekst tijdelijk bijhouden voor de CV-preview (enkel in het geheugen
# van deze sessie; wordt gewist bij een nieuwe analyse)
if "cv_bestand_bytes" not in st.session_state:
    st.session_state.cv_bestand_bytes = None
if "cv_extensie" not in st.session_state:
    st.session_state.cv_extensie = ""
if "cv_tekst" not in st.session_state:
    st.session_state.cv_tekst = ""

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


# Zelfde CV-tekst + zelfde criteria + zelfde taal → exact hetzelfde rapport.
# De cache leeft enkel in het geheugen (max. 2 uur), er wordt niets op schijf bewaard.
@st.cache_data(ttl=7200, max_entries=200, show_spinner=False)
def _analyseer_gecached(cv_tekst: str, criteria_json: str, lang: str, extra_info: str) -> dict:
    return analyseer_cv(
        cv_tekst,
        criteria_override=json.loads(criteria_json) if criteria_json else None,
        lang=lang,
        extra_info=extra_info,
    )


def _controleer_api_sleutel() -> bool:
    sleutel = os.environ.get("ANTHROPIC_API_KEY", "")
    if not sleutel or not sleutel.startswith("sk-"):
        st.error(t("api_key_error"))
        return False
    return True


def _nieuwe_analyse():
    st.session_state.analyse_resultaat = None
    st.session_state.ocr_gebruikt = False
    st.session_state.cv_bestand_bytes = None
    st.session_state.cv_extensie = ""
    st.session_state.cv_tekst = ""
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
    if st.session_state.ocr_gebruikt:
        st.info(t("ocr_info"))
    toon_resultaten(
        st.session_state.analyse_resultaat,
        bestand_bytes=st.session_state.cv_bestand_bytes,
        extensie=st.session_state.cv_extensie,
        cv_tekst=st.session_state.cv_tekst,
    )
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
                tekst, melding = extraheer_tekst(pad)

            if not tekst:
                # Blokkerende fout: geen tekst gevonden
                st.warning(melding or t("error_no_text"))
                st.stop()

            # Niet-blokkerend: OCR werd gebruikt
            ocr_gebruikt = (melding == "ocr_gebruikt")

            # Technische gegevens (pagina's, lettergroottes) voor de lay-outcriteria
            bestand_bytes = bytes(bestand.getbuffer())
            extra_info = pdf_metadata(bestand_bytes) if extensie == ".pdf" else ""

            # Stap 2: analyse via Claude API (gecached: identieke input → identiek rapport)
            try:
                resultaat = _analyseer_gecached(
                    tekst,
                    json.dumps(criteria_override, sort_keys=True, ensure_ascii=False) if criteria_override else "",
                    st.session_state["lang"],
                    extra_info,
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
        st.session_state.ocr_gebruikt = ocr_gebruikt
        st.session_state.cv_bestand_bytes = bestand_bytes
        st.session_state.cv_extensie = extensie.lstrip(".")
        st.session_state.cv_tekst = tekst
        st.rerun()

# Voettekst
st.divider()
st.caption(t("footer"))
