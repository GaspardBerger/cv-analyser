#!/usr/bin/env python3
"""UI translations — NL / FR / EN."""

import streamlit as st

TRANSLATIONS: dict[str, dict[str, str]] = {
    "nl": {
        # app
        "app_header": "CV-Analysator",
        "app_subtitle": (
            "Ontdek hoe sterk jouw CV is en wat je kunt verbeteren. "
            "Upload je CV hieronder — je gegevens worden **niet bewaard** na de analyse."
        ),
        "api_key_error": (
            "**API-sleutel niet gevonden.**\n\n"
            "Maak een bestand aan genaamd `.env` in de map `cv-analysator/` "
            "met de volgende inhoud:\n\n```\nANTHROPIC_API_KEY=jouw-sleutel-hier\n```\n\n"
            "Herstart daarna de applicatie."
        ),
        "btn_new_analysis": "Nieuw CV analyseren",
        "btn_analyse": "CV analyseren",
        "spinner": "Je CV wordt geanalyseerd…",
        "error_no_text": "Er kon geen tekst worden uitgelezen uit het bestand.",
        "error_no_connection": (
            "Geen verbinding met de analyseservice. "
            "Controleer je internetverbinding en probeer het opnieuw."
        ),
        "error_unexpected": "Er is een onverwachte fout opgetreden: {error}",
        "footer": "Gluon Educatie — CV-Analysator v1.0 | Gegevens worden niet opgeslagen",
        # upload
        "upload_header": "### Jouw CV uploaden",
        "upload_caption": "Ondersteunde formaten: PDF en Word (.docx) — maximaal 10 MB",
        "upload_label": "Kies je CV",
        "upload_help": "Sleep je CV hierheen of klik om een bestand te kiezen.",
        "upload_error_size": "Het bestand is te groot ({size:.1f} MB). Maximale bestandsgrootte is {max} MB.",
        "upload_error_type": "Bestandstype '.{ext}' wordt niet ondersteund. Upload een PDF- of Word-bestand (.docx).",
        "upload_success": "Bestand geladen: **{name}** ({size:.2f} MB)",
        "upload_filename_tip": "Tip voor de bestandsnaam: gebruik bij voorkeur **Cv_Voornaam Naam.pdf** (bijv. Cv_Jana Claes.pdf). Je kunt ook 'student' en de functie toevoegen: Cv_Jana Claes student Onthaal.pdf",
        # results
        "results_header": "## Resultaten van je CV-analyse",
        "results_summary": "**Samenvatting**",
        "results_cat_scores": "### Score per categorie",
        "results_strengths": "### Wat je al goed doet",
        "results_improvements": "### Hoe je je CV kunt verbeteren",
        "results_improvements_caption": "{n} verbeterpunt{p}, van meest naar minst impactvol",
        "results_improvements_plural": "en",
        "results_what_missing": "**Wat ontbreekt:**",
        "results_why_important": "**Waarom dit belangrijk is:**",
        "results_example": "**Concreet voorbeeld:**",
        "results_cv_lang": "CV-taal gedetecteerd: {lang}",
        # score labels (internal English keys → display text)
        "score_needs_work": "Vereist veel werk",
        "score_sufficient": "Voldoende",
        "score_good": "Goed",
        "score_very_good": "Zeer goed",
        "score_excellent": "Uitstekend",
        "score_unknown": "Onbekend",
        # category names
        "cat_structuur_opmaak": "Structuur & Opmaak",
        "cat_inhoud": "Inhoud",
        "cat_taal_schrijfstijl": "Taal & Schrijfstijl",
        "cat_professionaliteit": "Professionaliteit",
        # priority labels
        "prio_1": "Hoogste prioriteit",
        "prio_2": "Hoge prioriteit",
        "prio_3": "Gemiddelde prioriteit",
        "prio_4": "Lage prioriteit",
        "prio_5": "Lage prioriteit",
        # CV language names
        "cv_lang_nl": "Nederlands",
        "cv_lang_fr": "Frans",
        "cv_lang_en": "Engels",
        # criteria editor
        "criteria_expander": "Criteria aanpassen (voor begeleiders)",
        "criteria_caption": (
            "Hier kun je criteria aan- of uitzetten en beschrijvingen aanpassen voor deze sessie. "
            "Wijzigingen worden **niet** opgeslagen en verdwijnen wanneer de pagina wordt vernieuwd."
        ),
        "criteria_reset": "Standaard criteria herstellen",
        "criteria_weight": "huidig gewicht: {weight}%",
        "criteria_context_header": "**Contextuele instellingen**",
        "criteria_doelgroep": "Doelgroep",
        "criteria_active_info": "Aangepaste criteria zijn actief voor deze sessie.",
        "criteria_yaml_expander": "Huidige criteria bekijken (YAML)",
        "criteria_yaml_caption": "Wil je criteria permanent opslaan? Pas het bestand aan: `{path}`",
        # system prompt
        "system_lang_instruction": "geef de analyse in het Nederlands",
    },
    "fr": {
        # app
        "app_header": "Analyseur de CV",
        "app_subtitle": (
            "Découvrez les points forts de votre CV et comment l'améliorer. "
            "Téléchargez votre CV ci-dessous — vos données ne sont **pas conservées** après l'analyse."
        ),
        "api_key_error": (
            "**Clé API introuvable.**\n\n"
            "Créez un fichier `.env` dans le dossier `cv-analysator/` avec le contenu suivant :\n\n"
            "```\nANTHROPIC_API_KEY=votre-clé-ici\n```\n\n"
            "Redémarrez ensuite l'application."
        ),
        "btn_new_analysis": "Analyser un nouveau CV",
        "btn_analyse": "Analyser le CV",
        "spinner": "Votre CV est en cours d'analyse…",
        "error_no_text": "Aucun texte n'a pu être extrait du fichier.",
        "error_no_connection": (
            "Impossible de se connecter au service d'analyse. "
            "Vérifiez votre connexion internet et réessayez."
        ),
        "error_unexpected": "Une erreur inattendue s'est produite : {error}",
        "footer": "Gluon Educatie — Analyseur de CV v1.0 | Les données ne sont pas conservées",
        # upload
        "upload_header": "### Télécharger votre CV",
        "upload_caption": "Formats acceptés : PDF et Word (.docx) — 10 Mo maximum",
        "upload_label": "Choisir votre CV",
        "upload_help": "Faites glisser votre CV ici ou cliquez pour choisir un fichier.",
        "upload_error_size": "Le fichier est trop volumineux ({size:.1f} Mo). La taille maximale est de {max} Mo.",
        "upload_error_type": "Le type de fichier '.{ext}' n'est pas pris en charge. Téléchargez un fichier PDF ou Word (.docx).",
        "upload_success": "Fichier chargé : **{name}** ({size:.2f} Mo)",
        "upload_filename_tip": "Conseil sur le nom du fichier : utilisez de préférence **Cv_Prénom Nom.pdf** (ex. Cv_Jana Claes.pdf). Vous pouvez aussi ajouter 'étudiant' et la fonction visée : Cv_Jana Claes étudiant Accueil.pdf",
        # results
        "results_header": "## Résultats de l'analyse de votre CV",
        "results_summary": "**Résumé**",
        "results_cat_scores": "### Score par catégorie",
        "results_strengths": "### Ce que vous faites déjà bien",
        "results_improvements": "### Comment améliorer votre CV",
        "results_improvements_caption": "{n} point{p} d'amélioration, du plus au moins impactant",
        "results_improvements_plural": "s",
        "results_what_missing": "**Ce qui manque :**",
        "results_why_important": "**Pourquoi c'est important :**",
        "results_example": "**Exemple concret :**",
        "results_cv_lang": "Langue du CV détectée : {lang}",
        # score labels
        "score_needs_work": "À améliorer",
        "score_sufficient": "Suffisant",
        "score_good": "Bien",
        "score_very_good": "Très bien",
        "score_excellent": "Excellent",
        "score_unknown": "Inconnu",
        # category names
        "cat_structuur_opmaak": "Structure & Mise en page",
        "cat_inhoud": "Contenu",
        "cat_taal_schrijfstijl": "Langue & Style",
        "cat_professionaliteit": "Professionnalisme",
        # priority labels
        "prio_1": "Priorité maximale",
        "prio_2": "Haute priorité",
        "prio_3": "Priorité moyenne",
        "prio_4": "Faible priorité",
        "prio_5": "Faible priorité",
        # CV language names
        "cv_lang_nl": "Néerlandais",
        "cv_lang_fr": "Français",
        "cv_lang_en": "Anglais",
        # criteria editor
        "criteria_expander": "Modifier les critères (pour les formateurs)",
        "criteria_caption": (
            "Vous pouvez activer ou désactiver des critères et modifier les descriptions pour cette session. "
            "Les modifications ne sont **pas enregistrées** et disparaissent lors du rechargement de la page."
        ),
        "criteria_reset": "Rétablir les critères par défaut",
        "criteria_weight": "poids actuel : {weight}%",
        "criteria_context_header": "**Paramètres contextuels**",
        "criteria_doelgroep": "Groupe cible",
        "criteria_active_info": "Les critères modifiés sont actifs pour cette session.",
        "criteria_yaml_expander": "Voir les critères actuels (YAML)",
        "criteria_yaml_caption": "Vous souhaitez enregistrer les critères de façon permanente ? Modifiez le fichier : `{path}`",
        # system prompt
        "system_lang_instruction": "donne l'analyse en français",
    },
    "en": {
        # app
        "app_header": "CV Analyser",
        "app_subtitle": (
            "Discover how strong your CV is and what you can improve. "
            "Upload your CV below — your data is **not stored** after the analysis."
        ),
        "api_key_error": (
            "**API key not found.**\n\n"
            "Create a file named `.env` in the `cv-analysator/` folder with the following content:\n\n"
            "```\nANTHROPIC_API_KEY=your-key-here\n```\n\n"
            "Then restart the application."
        ),
        "btn_new_analysis": "Analyse a new CV",
        "btn_analyse": "Analyse CV",
        "spinner": "Your CV is being analysed…",
        "error_no_text": "No text could be extracted from the file.",
        "error_no_connection": (
            "Unable to connect to the analysis service. "
            "Check your internet connection and try again."
        ),
        "error_unexpected": "An unexpected error occurred: {error}",
        "footer": "Gluon Educatie — CV Analyser v1.0 | Data is not stored",
        # upload
        "upload_header": "### Upload your CV",
        "upload_caption": "Supported formats: PDF and Word (.docx) — maximum 10 MB",
        "upload_label": "Choose your CV",
        "upload_help": "Drag your CV here or click to choose a file.",
        "upload_error_size": "The file is too large ({size:.1f} MB). Maximum file size is {max} MB.",
        "upload_error_type": "File type '.{ext}' is not supported. Upload a PDF or Word file (.docx).",
        "upload_success": "File loaded: **{name}** ({size:.2f} MB)",
        "upload_filename_tip": "File name tip: preferably use **Cv_FirstName LastName.pdf** (e.g. Cv_Jana Claes.pdf). You can also add 'student' and the job function: Cv_Jana Claes student Reception.pdf",
        # results
        "results_header": "## Results of your CV analysis",
        "results_summary": "**Summary**",
        "results_cat_scores": "### Score per category",
        "results_strengths": "### What you're already doing well",
        "results_improvements": "### How to improve your CV",
        "results_improvements_caption": "{n} improvement point{p}, from most to least impactful",
        "results_improvements_plural": "s",
        "results_what_missing": "**What is missing:**",
        "results_why_important": "**Why this matters:**",
        "results_example": "**Concrete example:**",
        "results_cv_lang": "CV language detected: {lang}",
        # score labels
        "score_needs_work": "Needs work",
        "score_sufficient": "Sufficient",
        "score_good": "Good",
        "score_very_good": "Very good",
        "score_excellent": "Excellent",
        "score_unknown": "Unknown",
        # category names
        "cat_structuur_opmaak": "Structure & Layout",
        "cat_inhoud": "Content",
        "cat_taal_schrijfstijl": "Language & Style",
        "cat_professionaliteit": "Professionalism",
        # priority labels
        "prio_1": "Highest priority",
        "prio_2": "High priority",
        "prio_3": "Medium priority",
        "prio_4": "Low priority",
        "prio_5": "Low priority",
        # CV language names
        "cv_lang_nl": "Dutch",
        "cv_lang_fr": "French",
        "cv_lang_en": "English",
        # criteria editor
        "criteria_expander": "Adjust criteria (for trainers)",
        "criteria_caption": (
            "You can enable or disable criteria and edit descriptions for this session. "
            "Changes are **not saved** and disappear when the page is refreshed."
        ),
        "criteria_reset": "Restore default criteria",
        "criteria_weight": "current weight: {weight}%",
        "criteria_context_header": "**Contextual settings**",
        "criteria_doelgroep": "Target group",
        "criteria_active_info": "Modified criteria are active for this session.",
        "criteria_yaml_expander": "View current criteria (YAML)",
        "criteria_yaml_caption": "Want to save criteria permanently? Edit the file: `{path}`",
        # system prompt
        "system_lang_instruction": "give the analysis in English",
    },
}

LANGUAGE_OPTIONS: dict[str, str] = {
    "Nederlands": "nl",
    "Français": "fr",
    "English": "en",
}


def t(key: str, **kwargs) -> str:
    """Return the translated string for the current UI language."""
    lang = st.session_state.get("lang", "nl")
    text = TRANSLATIONS.get(lang, TRANSLATIONS["nl"]).get(
        key, TRANSLATIONS["nl"].get(key, key)
    )
    return text.format(**kwargs) if kwargs else text
