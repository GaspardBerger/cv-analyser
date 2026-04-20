#!/usr/bin/env python3
"""Weergave van analyseresultaten: score, verbeterpunten en sterke punten."""

import streamlit as st

SCORE_KLEUREN = {
    "Vereist veel werk": "#e74c3c",
    "Voldoende": "#e67e22",
    "Goed": "#f1c40f",
    "Zeer goed": "#2ecc71",
    "Uitstekend": "#27ae60",
}

CATEGORIE_NAMEN = {
    "structuur_opmaak": "Structuur & Opmaak",
    "inhoud": "Inhoud",
    "taal_schrijfstijl": "Taal & Schrijfstijl",
    "professionaliteit": "Professionaliteit",
}

PRIORITEIT_LABELS = {1: "Hoogste prioriteit", 2: "Hoge prioriteit", 3: "Gemiddelde prioriteit", 4: "Lage prioriteit", 5: "Lage prioriteit"}


def toon_resultaten(resultaat: dict) -> None:
    """Toon de volledige analyseresultaten op het scherm."""
    score = resultaat.get("totaalscore", 0)
    label = resultaat.get("score_label", "")
    kleur = SCORE_KLEUREN.get(label, "#95a5a6")

    st.divider()
    st.markdown("## Resultaten van je CV-analyse")

    # Totaalscore
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            f"""
            <div style="
                background-color: {kleur};
                border-radius: 16px;
                padding: 24px;
                text-align: center;
                color: white;
            ">
                <div style="font-size: 52px; font-weight: bold;">{score}</div>
                <div style="font-size: 18px; margin-top: 4px;">/100</div>
                <div style="font-size: 16px; margin-top: 8px; font-weight: 600;">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        samenvatting = resultaat.get("samenvatting", "")
        if samenvatting:
            st.markdown(f"**Samenvatting**\n\n{samenvatting}")

    # Categoriescores
    st.markdown("### Score per categorie")
    categorie_scores = resultaat.get("categorie_scores", {})
    kolommen = st.columns(len(categorie_scores))

    for (cat_id, cat_data), col in zip(categorie_scores.items(), kolommen):
        cat_score = cat_data.get("score", 0)
        cat_max = cat_data.get("max", 0)
        cat_label = cat_data.get("label", "")
        cat_naam = CATEGORIE_NAMEN.get(cat_id, cat_id)
        percentage = int((cat_score / cat_max * 100)) if cat_max else 0
        cat_kleur = SCORE_KLEUREN.get(cat_label, "#95a5a6")

        with col:
            st.markdown(
                f"""
                <div style="
                    border: 2px solid {cat_kleur};
                    border-radius: 10px;
                    padding: 14px;
                    text-align: center;
                    margin-bottom: 8px;
                ">
                    <div style="font-size: 22px; font-weight: bold; color: {cat_kleur};">{cat_score}/{cat_max}</div>
                    <div style="font-size: 12px; color: #666; margin-top: 4px;">{cat_naam}</div>
                    <div style="font-size: 12px; font-weight: 600; color: {cat_kleur};">{cat_label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(percentage / 100)

    # Sterke punten
    sterke_punten = resultaat.get("sterke_punten", [])
    if sterke_punten:
        st.markdown("### Wat je al goed doet")
        for punt in sterke_punten:
            st.success(f"✓ {punt}")

    # Verbeterpunten
    verbeterpunten = resultaat.get("verbeterpunten", [])
    if verbeterpunten:
        st.markdown("### Hoe je je CV kunt verbeteren")
        st.caption(f"{len(verbeterpunten)} verbeterpunt{'en' if len(verbeterpunten) > 1 else ''}, van meest naar minst impactvol")

        for vp in verbeterpunten:
            prioriteit = vp.get("prioriteit", 1)
            titel = vp.get("titel", "")
            probleem = vp.get("probleem", "")
            waarom = vp.get("waarom", "")
            voorbeeld = vp.get("voorbeeld", "")
            cat = CATEGORIE_NAMEN.get(vp.get("categorie", ""), vp.get("categorie", ""))
            prio_label = PRIORITEIT_LABELS.get(prioriteit, "")

            with st.expander(f"**{prioriteit}. {titel}** — {cat}", expanded=(prioriteit <= 2)):
                if prio_label:
                    st.caption(prio_label)
                if probleem:
                    st.markdown(f"**Wat ontbreekt:** {probleem}")
                if waarom:
                    st.markdown(f"**Waarom dit belangrijk is:** {waarom}")
                if voorbeeld:
                    st.info(f"**Concreet voorbeeld:** {voorbeeld}")

    # Taalindicator
    taal = resultaat.get("taal_cv", "")
    taal_namen = {"nl": "Nederlands", "fr": "Frans", "en": "Engels"}
    if taal:
        st.caption(f"CV-taal gedetecteerd: {taal_namen.get(taal, taal.upper())}")
