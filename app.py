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
from ui.criteria_editor import toon_criteria_editor
from ui.results import toon_resultaten
from ui.upload import toon_upload_widget


st.set_page_config(
    page_title="CV-Analysator — Gluon Educatie",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Sessie-state initialiseren
if "analyse_resultaat" not in st.session_state:
    st.session_state.analyse_resultaat = None
if "criteria_override" not in st.session_state:
    st.session_state.criteria_override = None


def _controleer_api_sleutel() -> bool:
    sleutel = os.environ.get("ANTHROPIC_API_KEY", "")
    if not sleutel or not sleutel.startswith("sk-"):
        st.error(
            "**API-sleutel niet gevonden.**\n\n"
            "Maak een bestand aan genaamd `.env` in de map `cv-analysator/` "
            "met de volgende inhoud:\n\n```\nANTHROPIC_API_KEY=jouw-sleutel-hier\n```\n\n"
            "Herstart daarna de applicatie."
        )
        return False
    return True


def _nieuwe_analyse():
    """Verwijder het vorige resultaat zodat de gebruiker opnieuw kan starten."""
    st.session_state.analyse_resultaat = None
    st.rerun()


# Header
st.markdown("# CV-Analysator")
st.markdown(
    "Ontdek hoe sterk jouw CV is en wat je kunt verbeteren. "
    "Upload je CV hieronder — je gegevens worden **niet bewaard** na de analyse."
)
st.divider()

# API-sleutel controleren
if not _controleer_api_sleutel():
    st.stop()

# Toon resultaten als analyse al gedaan is
if st.session_state.analyse_resultaat is not None:
    toon_resultaten(st.session_state.analyse_resultaat)
    st.divider()
    if st.button("Nieuw CV analyseren", type="secondary"):
        _nieuwe_analyse()
    st.stop()

# Upload-widget
bestand = toon_upload_widget()

# Criteria-editor voor begeleiders
criteria_override = toon_criteria_editor()

# Analyseknop
if bestand is not None:
    st.divider()
    if st.button("CV analyseren", type="primary", use_container_width=True):
        extensie = "." + bestand.name.rsplit(".", 1)[-1].lower()

        with st.spinner("Je CV wordt geanalyseerd…"):
            # Stap 1: tekst extraheren (tijdelijk bestand, direct verwijderd)
            with tijdelijk_bestand(bestand, extensie) as pad:
                tekst, waarschuwing = extraheer_tekst(pad)

            if waarschuwing:
                st.warning(waarschuwing)
                st.stop()

            if not tekst:
                st.error("Er kon geen tekst worden uitgelezen uit het bestand.")
                st.stop()

            # Stap 2: analyse via Claude API
            try:
                resultaat = analyseer_cv(tekst, criteria_override=criteria_override)
            except RuntimeError as fout:
                st.error(str(fout))
                st.stop()
            except Exception as fout:
                fout_str = str(fout).lower()
                if "connection" in fout_str or "network" in fout_str or "timeout" in fout_str:
                    st.error(
                        "Geen verbinding met de analyseservice. "
                        "Controleer je internetverbinding en probeer het opnieuw."
                    )
                else:
                    st.error(f"Er is een onverwachte fout opgetreden: {fout}")
                st.stop()

        st.session_state.analyse_resultaat = resultaat
        st.rerun()

# Voettekst
st.divider()
st.caption("Gluon Educatie — CV-Analysator v1.0 | Gegevens worden niet opgeslagen")
