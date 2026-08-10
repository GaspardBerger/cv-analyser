#!/usr/bin/env python3
"""Weergave van analyseresultaten.

Opbouw (zoals de schets): score bovenaan, daaronder twee kolommen —
links de genummerde verbeterpunten (fouten eerst), rechts de CV-preview
waarop de fouten met stippellijnkaders en nummers zijn aangeduid.
Daaronder: sterke punten, de volledige criteria-checklist en de adrescontrole.
"""

import streamlit as st

from core.preview import render_pdf_met_markeringen, tekst_preview_html
from translations import t

# Internal English score keys → hex color
SCORE_KLEUREN = {
    "needs_work": "#e74c3c",
    "sufficient": "#e67e22",
    "good": "#f1c40f",
    "very_good": "#2ecc71",
    "excellent": "#27ae60",
}


def toon_resultaten(
    resultaat: dict,
    bestand_bytes: bytes | None = None,
    extensie: str = "",
    cv_tekst: str = "",
) -> None:
    """Toon de volledige analyseresultaten op het scherm."""
    st.divider()
    st.markdown(t("results_header"))
    _toon_score(resultaat)
    _toon_categorie_scores(resultaat)

    verbeterpunten = resultaat.get("verbeterpunten", [])

    # Preview voorbereiden (bepaalt ook welke punten op het CV gemarkeerd zijn)
    preview_afbeeldingen: list[bytes] = []
    preview_html = ""
    gemarkeerd: set[int] = set()
    if bestand_bytes and extensie == "pdf":
        preview_afbeeldingen, gemarkeerd = render_pdf_met_markeringen(
            bestand_bytes, verbeterpunten
        )
    if not preview_afbeeldingen and cv_tekst:
        preview_html, gemarkeerd = tekst_preview_html(cv_tekst, verbeterpunten)

    # Twee kolommen: links de fouten, rechts de CV-preview
    st.divider()
    links, rechts = st.columns([1, 1], gap="medium")

    with links:
        st.markdown(t("results_improvements"))
        if verbeterpunten:
            n = len(verbeterpunten)
            plural = t("results_improvements_plural") if n > 1 else ""
            st.caption(t("results_improvements_caption", n=n, p=plural))
            for vp in verbeterpunten:
                _toon_verbeterpunt(vp, gemarkeerd)
        else:
            st.success(t("results_no_improvements"))

    with rechts:
        st.markdown(t("results_preview_header"))
        if preview_afbeeldingen:
            for afbeelding in preview_afbeeldingen:
                st.image(afbeelding, use_container_width=True)
        elif preview_html:
            st.caption(t("results_preview_text_note"))
            st.markdown(preview_html, unsafe_allow_html=True)
        else:
            st.info(t("results_preview_unavailable"))

    # Sterke punten (na de fouten)
    sterke_punten = resultaat.get("sterke_punten", [])
    if sterke_punten:
        st.divider()
        st.markdown(t("results_strengths"))
        for punt in sterke_punten:
            st.success(f"✓ {punt}")

    _toon_checklist(resultaat)
    _toon_adres_check(resultaat)

    # Taalindicator
    taal = resultaat.get("taal_cv", "")
    if taal:
        taal_naam = t(f"cv_lang_{taal}")
        st.caption(t("results_cv_lang", lang=taal_naam))


def _toon_score(resultaat: dict) -> None:
    score = resultaat.get("totaalscore", 0)
    score_key = resultaat.get("score_label", "")
    label = t(f"score_{score_key}") if score_key else ""
    kleur = SCORE_KLEUREN.get(score_key, "#95a5a6")

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


def _toon_categorie_scores(resultaat: dict) -> None:
    categorie_scores = resultaat.get("categorie_scores", {})
    if not categorie_scores:
        return
    st.markdown(t("results_cat_scores"))
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


def _toon_verbeterpunt(vp: dict, gemarkeerd: set[int]) -> None:
    prioriteit = vp.get("prioriteit", 1)
    titel = vp.get("titel", "")
    probleem = vp.get("probleem", "")
    waarom = vp.get("waarom", "")
    voorbeeld = vp.get("voorbeeld", "")
    cat = t(f"cat_{vp.get('categorie', '')}")

    with st.expander(f"**{prioriteit}. {titel}** — {cat}", expanded=(prioriteit <= 3)):
        if prioriteit in gemarkeerd:
            st.caption(t("results_see_marker", n=prioriteit))
        if probleem:
            st.markdown(f"{t('results_what_missing')} {probleem}")
        if waarom:
            st.markdown(f"{t('results_why_important')} {waarom}")
        if voorbeeld:
            st.info(f"{t('results_example')} {voorbeeld}")


def _toon_checklist(resultaat: dict) -> None:
    checklist = resultaat.get("criteria_checklist", [])
    if not checklist:
        return
    st.divider()
    st.markdown(t("results_checklist"))
    st.caption(t("results_checklist_caption"))
    per_categorie: dict[str, list[dict]] = {}
    for item in checklist:
        per_categorie.setdefault(item["categorie"], []).append(item)

    for cat_id, items in per_categorie.items():
        volledig = sum(1 for i in items if i.get("score", 0) >= 1)
        titel = f"{t(f'cat_{cat_id}')} — {volledig}/{len(items)} {t('checklist_complete')}"
        with st.expander(titel, expanded=False):
            for item in items:
                item_score = item.get("score", 0)
                if item_score >= 1:
                    icoon, status = "✅", t("checklist_met")
                elif item_score >= 0.5:
                    icoon, status = "🟡", t("checklist_partial")
                else:
                    icoon, status = "❌", t("checklist_not_met")
                handmatig = f" 👁️ {t('checklist_manual')}" if item.get("handmatig") else ""
                st.markdown(f"{icoon} **{status}**{handmatig} — {item['beschrijving']}")
                if item.get("toelichting"):
                    st.caption(item["toelichting"])


def _toon_adres_check(resultaat: dict) -> None:
    adres_check = resultaat.get("adres_check") or {}
    if not adres_check:
        return
    st.markdown(t("results_adres_header"))
    adres = adres_check.get("adres", "")
    opmerking = adres_check.get("opmerking", "")
    if not adres_check.get("adres_gevonden"):
        st.info(t("adres_none"))
    elif adres_check.get("komt_overeen"):
        st.success(t("adres_ok", adres=adres))
    else:
        st.warning(t("adres_mismatch", adres=adres) + (f" {opmerking}" if opmerking else ""))
