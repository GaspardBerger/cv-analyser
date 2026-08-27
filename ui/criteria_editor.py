#!/usr/bin/env python3
"""Criteriaoverzicht.

Voor deelnemers is dit een alleen-lezen lijst: ze zien elk criterium waarop hun
CV beoordeeld wordt, maar kunnen er niets aan wijzigen.

Begeleiders kunnen de criteria wél aanpassen en eigen criteria toevoegen, na
het invoeren van de begeleiderscode. Die code stel je in als `TRAINER_CODE`
bij de secrets van de app (of als omgevingsvariabele). Is er geen code
ingesteld, dan blijft het scherm voor iedereen alleen-lezen.
"""

import copy
import os
import re

import streamlit as st

from core.analyzer import laad_criteria
from translations import t


def _ingestelde_code() -> str:
    """Lees de begeleiderscode uit de secrets of de omgeving."""
    try:
        if "TRAINER_CODE" in st.secrets:
            return str(st.secrets["TRAINER_CODE"]).strip()
    except Exception:
        pass
    return os.environ.get("TRAINER_CODE", "").strip()


def _toon_alleen_lezen(criteria: dict) -> None:
    """Toon de criteria als leeslijst, zonder invoervelden."""
    for cat in criteria.get("categorieen", {}).values():
        actief = [c for c in cat.get("criteria", []) if c.get("actief", True)]
        st.markdown(f"**{cat['naam']}** ({t('criteria_weight', weight=cat['gewicht'])})")
        for criterium in actief:
            st.markdown(f"- {criterium['beschrijving']}")
        st.markdown("---")


def toon_criteria_editor() -> dict | None:
    """
    Toon het criteriaoverzicht. Geeft de aangepaste criteria terug als een
    begeleider ze gewijzigd heeft, anders None (= standaardcriteria).
    """
    with st.expander(t("criteria_expander"), expanded=False):
        code = _ingestelde_code()
        ontgrendeld = bool(st.session_state.get("criteria_ontgrendeld"))
        standaard = laad_criteria()
        huidig = st.session_state.get("criteria_override") or standaard

        if not ontgrendeld:
            st.caption(t("criteria_readonly_caption"))
            _toon_alleen_lezen(huidig)
            if code:
                with st.form("criteria_ontgrendelen"):
                    ingave = st.text_input(t("criteria_code_label"), type="password")
                    if st.form_submit_button(t("criteria_code_btn")):
                        if ingave and ingave == code:
                            st.session_state["criteria_ontgrendeld"] = True
                            st.rerun()
                        else:
                            st.error(t("criteria_code_fout"))
            else:
                st.caption(t("criteria_locked_note"))
            return st.session_state.get("criteria_override")

        # ── Vanaf hier: begeleidersmodus ──
        st.caption(t("criteria_caption"))

        kol_a, kol_b = st.columns(2)
        with kol_a:
            if st.button(t("criteria_reset"), key="reset_criteria"):
                st.session_state.pop("criteria_override", None)
                st.rerun()
        with kol_b:
            if st.button(t("criteria_lock"), key="lock_criteria"):
                st.session_state["criteria_ontgrendeld"] = False
                st.rerun()

        criteria_werk = copy.deepcopy(huidig)
        gewijzigd = False
        categorieen = criteria_werk.get("categorieen", {})

        for cat_id, cat in categorieen.items():
            st.markdown(f"**{cat['naam']}** ({t('criteria_weight', weight=cat['gewicht'])})")

            nieuw_gewicht = st.slider(
                f"Gewicht {cat['naam']}",
                min_value=0,
                max_value=50,
                value=int(cat["gewicht"]),
                key=f"gewicht_{cat_id}",
                label_visibility="collapsed",
            )
            if nieuw_gewicht != cat["gewicht"]:
                categorieen[cat_id]["gewicht"] = nieuw_gewicht
                gewijzigd = True

            for i, criterium in enumerate(cat["criteria"]):
                col1, col2 = st.columns([0.1, 0.9])
                with col1:
                    actief = st.checkbox(
                        "Actief",
                        value=criterium.get("actief", True),
                        key=f"actief_{cat_id}_{criterium['id']}",
                        label_visibility="collapsed",
                    )
                with col2:
                    nieuwe_beschrijving = st.text_input(
                        criterium["id"],
                        value=criterium["beschrijving"],
                        key=f"beschr_{cat_id}_{criterium['id']}",
                        label_visibility="collapsed",
                    )

                if actief != criterium.get("actief", True):
                    categorieen[cat_id]["criteria"][i]["actief"] = actief
                    gewijzigd = True

                if nieuwe_beschrijving != criterium["beschrijving"]:
                    categorieen[cat_id]["criteria"][i]["beschrijving"] = nieuwe_beschrijving
                    gewijzigd = True

            # Eigen criterium toevoegen aan deze categorie
            col_input, col_btn = st.columns([0.75, 0.25])
            with col_input:
                nieuw_criterium = st.text_input(
                    t("criteria_new_label"),
                    key=f"nieuw_{cat_id}",
                    placeholder=t("criteria_new_placeholder"),
                    label_visibility="collapsed",
                )
            with col_btn:
                toevoegen = st.button(t("criteria_new_btn"), key=f"nieuw_btn_{cat_id}")
            if toevoegen and nieuw_criterium.strip():
                bestaande_ids = {c["id"] for c in cat["criteria"]}
                basis_id = re.sub(r"[^a-z0-9]+", "_", nieuw_criterium.lower()).strip("_")[:40] or "eigen_criterium"
                nieuw_id = basis_id
                teller = 2
                while nieuw_id in bestaande_ids:
                    nieuw_id = f"{basis_id}_{teller}"
                    teller += 1
                categorieen[cat_id]["criteria"].append({
                    "id": nieuw_id,
                    "beschrijving": nieuw_criterium.strip(),
                    "verplicht": False,
                    "gewicht": 1,
                    "actief": True,
                })
                st.session_state["criteria_override"] = criteria_werk
                st.rerun()

            st.markdown("---")

        # Context-instellingen
        st.markdown(t("criteria_context_header"))
        context = criteria_werk.get("context", {})
        nieuwe_doelgroep = st.text_input(
            t("criteria_doelgroep"),
            value=context.get("doelgroep", ""),
            key="context_doelgroep",
        )
        if nieuwe_doelgroep != context.get("doelgroep", ""):
            criteria_werk["context"]["doelgroep"] = nieuwe_doelgroep
            gewijzigd = True

        if gewijzigd:
            st.session_state["criteria_override"] = criteria_werk
            st.info(t("criteria_active_info"))
            return criteria_werk

    return st.session_state.get("criteria_override")
