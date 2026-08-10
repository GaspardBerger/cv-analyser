#!/usr/bin/env python3
"""Trainer-interface voor het tijdelijk aanpassen en toevoegen van CV-criteria binnen een sessie."""

import copy
import re

import streamlit as st
import yaml

from core.analyzer import laad_criteria, CRITERIA_PAD
from translations import t


def toon_criteria_editor() -> dict | None:
    """
    Toon een uitklapbare editor waarmee begeleiders de criteria kunnen aanpassen.
    Wijzigingen gelden alleen voor de huidige sessie en worden niet opgeslagen.
    Geeft de aangepaste criteria terug als dict, of None als de standaard criteria gebruikt worden.
    """
    with st.expander(t("criteria_expander"), expanded=False):
        st.caption(t("criteria_caption"))

        if st.button(t("criteria_reset"), key="reset_criteria"):
            if "criteria_override" in st.session_state:
                del st.session_state["criteria_override"]
            st.rerun()

        standaard = laad_criteria()
        criteria_werk = copy.deepcopy(
            st.session_state.get("criteria_override") or standaard
        )

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

                if not actief:
                    categorieen[cat_id]["criteria"][i]["actief"] = False
                    gewijzigd = True
                elif "actief" in criterium and not criterium["actief"]:
                    categorieen[cat_id]["criteria"][i]["actief"] = True
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

        # Toon ook YAML-exportoptie voor permanente opslag
        with st.expander(t("criteria_yaml_expander"), expanded=False):
            st.code(yaml.dump(standaard, allow_unicode=True, default_flow_style=False), language="yaml")
            st.caption(t("criteria_yaml_caption", path=CRITERIA_PAD))

    return st.session_state.get("criteria_override")
