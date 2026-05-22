#!/usr/bin/env python3
"""Weergave van analyseresultaten: score, verbeterpunten en sterke punten."""

import streamlit as st

from translations import t

# Internal English score keys → hex color
SCORE_KLEUREN = {
    "needs_work": "#e74c3c",
    "sufficient": "#e67e22",
    "good": "#f1c40f",
    "very_good": "#2ecc71",
    "excellent": "#27ae60",
}


def toon_resultaten(resultaat: dict) -> None:
    """Toon de volledige analyseresultaten op het scherm."""
    score = resultaat.get("totaalscore", 0)
    score_key = resultaat.get("score_label", "")
    label = t(f"score_{score_key}") if score_key else ""
    kleur = SCORE_KLEUREN.get(score_key, "#95a5a6")

    st.divider()
    st.markdown(t("results_header"))

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
            st.markdown(f"{t('results_summary')}\n\n{samenvatting}")

    # Categoriescores
    st.markdown(t("results_cat_scores"))
    categorie_scores = resultaat.get("categorie_scores", {})
    kolommen = st.columns(len(categorie_scores))

    for (cat_id, cat_data), col in zip(categorie_scores.items(), kolommen):
        cat_score = cat_data.get("score", 0)
        cat_max = cat_data.get("max", 0)
        cat_score_key = cat_data.get("label", "")
        cat_label = t(f"score_{cat_score_key}") if cat_score_key else ""
        cat_naam = t(f"cat_{cat_id}")
        percentage = int((cat_score / cat_max * 100)) if cat_max else 0
        cat_kleur = SCORE_KLEUREN.get(cat_score_key, "#95a5a6")

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
        st.markdown(t("results_strengths"))
        for punt in sterke_punten:
            st.success(f"✓ {punt}")

    # Verbeterpunten
    verbeterpunten = resultaat.get("verbeterpunten", [])
    if verbeterpunten:
        st.markdown(t("results_improvements"))
        n = len(verbeterpunten)
        plural = t("results_improvements_plural") if n > 1 else ""
        st.caption(t("results_improvements_caption", n=n, p=plural))

        for vp in verbeterpunten:
            prioriteit = vp.get("prioriteit", 1)
            titel = vp.get("titel", "")
            probleem = vp.get("probleem", "")
            waarom = vp.get("waarom", "")
            voorbeeld = vp.get("voorbeeld", "")
            cat = t(f"cat_{vp.get('categorie', '')}")
            prio_label = t(f"prio_{prioriteit}")

            with st.expander(f"**{prioriteit}. {titel}** — {cat}", expanded=(prioriteit <= 2)):
                if prio_label:
                    st.caption(prio_label)
                if probleem:
                    st.markdown(f"{t('results_what_missing')} {probleem}")
                if waarom:
                    st.markdown(f"{t('results_why_important')} {waarom}")
                if voorbeeld:
                    st.info(f"{t('results_example')} {voorbeeld}")

    # Taalindicator
    taal = resultaat.get("taal_cv", "")
    if taal:
        taal_naam = t(f"cv_lang_{taal}")
        st.caption(t("results_cv_lang", lang=taal_naam))
