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
        "ocr_info": "Dit CV was een scan of afbeelding en kon niet rechtstreeks worden uitgelezen. De tekst werd herkend via AI (OCR) — de analyse is normaal bruikbaar, maar kan minder nauwkeurig zijn bij een onscherpe scan.",
        # privacy
        "privacy_short": "🔒 **Je CV wordt niet bewaard.** Er is geen database en geen account. Zodra je het tabblad sluit, is alles weg.",
        "privacy_header": "🔒 Wat gebeurt er precies met mijn gegevens?",
        "privacy_body": (
            "- **Je bestand wordt niet opgeslagen.** Het wordt heel even naar een tijdelijk bestand "
            "geschreven om de tekst eruit te lezen, en meteen daarna verwijderd.\n"
            "- **Er is geen database, geen account en geen logboek** met jouw gegevens. "
            "Niemand — ook je begeleider niet — kan je CV achteraf opvragen.\n"
            "- De tekst van je CV wordt via een beveiligde verbinding naar de Anthropic-API gestuurd "
            "om de analyse te maken. **Anthropic gebruikt deze tekst niet om AI-modellen te trainen.**\n"
            "- Zolang je dit venster openhoudt, blijft je resultaat in het werkgeheugen van de server staan. "
            "Daardoor krijg je exact dezelfde score als je hetzelfde CV opnieuw uploadt. "
            "Dat vervalt automatisch na maximaal 2 uur, of zodra je op “Nieuw CV analyseren” klikt.\n"
            "- **Sluit je het tabblad, dan is alles weg.**"
        ),
        # energie & CO2
        "impact_header": "🌱 Wat kost één analyse aan energie?",
        "impact_body": (
            "Eén CV analyseren kost naar schatting **{wh} Wh** ({kwh} kWh) en **{co2} g CO₂**.\n\n"
            "Dat is ongeveer evenveel als:\n"
            "- een **waterkoker** die {koker} seconden kookt\n"
            "- een **ledlamp** die {lamp} minuten brandt\n"
            "- {telefoon} analyses ≈ één keer je **smartphone opladen**\n"
            "- de CO₂ van **{auto} meter** met de auto rijden"
        ),
        "impact_note": (
            "Ruwe schatting, geen meting. Gebaseerd op publiek gerapporteerde cijfers "
            "(Google meldde in augustus 2025 een mediaan van 0,24 Wh voor één tekstprompt) "
            "en op de hoeveelheid tekst die deze app verstuurt en ontvangt. De echte waarde ligt "
            "vermoedelijk tussen 0,5 en 2 Wh. Bij een gescand CV of een JPG komt er tekstherkenning "
            "bij: reken dan op ongeveer het dubbele."
        ),
        # upload
        "upload_header": "### Jouw CV uploaden",
        "upload_caption": "Ondersteunde formaten: PDF, Word (.docx) en JPG — maximaal 10 MB",
        "upload_scan_note": (
            "📄 **Een PDF geeft het beste resultaat**: daarop kunnen we de fouten rechtstreeks aanduiden.\n\n"
            "📷 **Een JPG mag ook, maar enkel als scan van je CV** — dus niet een foto waarop ook je tafel, "
            "je handen of de achtergrond te zien zijn. Zorg dat het blad recht en scherp in beeld staat."
        ),
        "upload_scan_warning": (
            "Je uploadde een afbeelding. Controleer of dit een rechte, scherpe scan is van **enkel het CV**. "
            "Let op: op een afbeelding kunnen we de fouten niet met kaders aanduiden — je krijgt ze wel in de lijst."
        ),
        "upload_label": "Kies je CV",
        "upload_help": "Sleep je CV hierheen of klik om een bestand te kiezen.",
        "upload_error_size": "Het bestand is te groot ({size:.1f} MB). Maximale bestandsgrootte is {max} MB.",
        "upload_error_type": "Bestandstype '.{ext}' wordt niet ondersteund. Upload een PDF, een Word-bestand (.docx) of een scan in JPG.",
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
        "results_no_improvements": "Geen verbeterpunten gevonden — alles van de checklist is in orde!",
        # CV-preview
        "results_preview_header": "### CV-preview",
        "results_preview_text_note": "Voorbeeld op basis van de uitgelezen tekst — de originele lay-out kan afwijken.",
        "results_preview_image_note": "Op een scan of foto kunnen we geen kaders plaatsen. Hieronder staat de herkende tekst mét de markeringen.",
        "results_preview_unavailable": "Geen preview beschikbaar voor dit bestand.",
        "results_see_marker": "📍 Zie kader {n} op de CV-preview rechts",
        # criteria checklist
        "results_checklist": "### Alle beoordeelde criteria (de CV-checklist)",
        "results_checklist_caption": (
            "Dit zijn exact de criteria van de papieren CV-checklist — er zijn geen verborgen criteria. "
            "Als je alles van de checklist in orde brengt en je CV opnieuw uploadt, behaal je 100/100."
        ),
        "checklist_complete": "volledig in orde",
        "checklist_met": "Volledig aanwezig",
        "checklist_partial": "Gedeeltelijk aanwezig",
        "checklist_not_met": "Niet aanwezig",
        "checklist_points": "punten",
        "checklist_manual": "zelf visueel na te kijken",
        # address check
        "results_adres_header": "### Adrescontrole",
        "adres_none": "Er werd geen adres gevonden in het CV.",
        "adres_ok": "Het adres ({adres}) is in dezelfde taal geschreven als het CV. ✓",
        "adres_mismatch": "Let op: het adres ({adres}) lijkt niet in dezelfde taal geschreven als de rest van het CV.",
        # score labels (internal English keys → display text)
        "score_needs_work": "Vereist veel werk",
        "score_sufficient": "Voldoende",
        "score_good": "Goed",
        "score_very_good": "Zeer goed",
        "score_excellent": "Uitstekend",
        "score_unknown": "Onbekend",
        # category names
        "cat_lay_out": "Lay-out",
        "cat_inhoud": "Inhoud",
        "cat_structuur_opmaak": "Structuur & Opmaak",
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
        "criteria_expander": "🛠️ Criteria aanpassen of eigen criteria toevoegen (voor begeleiders)",
        "criteria_caption": (
            "Hier kun je criteria aan- of uitzetten, beschrijvingen aanpassen én per categorie "
            "eigen criteria toevoegen voor deze sessie. "
            "Wijzigingen worden **niet** opgeslagen en verdwijnen wanneer de pagina wordt vernieuwd."
        ),
        "criteria_new_label": "Nieuw criterium",
        "criteria_new_placeholder": "Beschrijf je eigen criterium en klik op 'Toevoegen'…",
        "criteria_new_btn": "➕ Toevoegen",
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
        "ocr_info": "Ce CV était un scan ou une image et n'a pas pu être lu directement. Le texte a été reconnu par IA (OCR) — l'analyse est normalement exploitable, mais peut être moins précise si le scan est flou.",
        # privacy
        "privacy_short": "🔒 **Votre CV n'est pas conservé.** Il n'y a ni base de données ni compte. Dès que vous fermez l'onglet, tout disparaît.",
        "privacy_header": "🔒 Que se passe-t-il exactement avec mes données ?",
        "privacy_body": (
            "- **Votre fichier n'est pas enregistré.** Il est écrit très brièvement dans un fichier temporaire "
            "pour en extraire le texte, puis supprimé immédiatement.\n"
            "- **Il n'y a ni base de données, ni compte, ni journal** contenant vos données. "
            "Personne — pas même votre formateur — ne peut consulter votre CV après coup.\n"
            "- Le texte de votre CV est envoyé via une connexion sécurisée à l'API d'Anthropic pour réaliser "
            "l'analyse. **Anthropic n'utilise pas ce texte pour entraîner ses modèles d'IA.**\n"
            "- Tant que vous gardez cette fenêtre ouverte, votre résultat reste dans la mémoire vive du serveur. "
            "Vous obtenez ainsi exactement le même score si vous téléchargez à nouveau le même CV. "
            "Cela expire automatiquement après 2 heures maximum, ou dès que vous cliquez sur « Analyser un nouveau CV ».\n"
            "- **Si vous fermez l'onglet, tout disparaît.**"
        ),
        # énergie & CO2
        "impact_header": "🌱 Combien d'énergie coûte une analyse ?",
        "impact_body": (
            "Analyser un CV coûte environ **{wh} Wh** ({kwh} kWh) et **{co2} g de CO₂**.\n\n"
            "Cela équivaut à peu près à :\n"
            "- une **bouilloire** qui chauffe pendant {koker} secondes\n"
            "- une **ampoule LED** allumée pendant {lamp} minutes\n"
            "- {telefoon} analyses ≈ une recharge complète de votre **smartphone**\n"
            "- le CO₂ de **{auto} mètres** parcourus en voiture"
        ),
        "impact_note": (
            "Estimation approximative, pas une mesure. Basée sur des chiffres publiés "
            "(en août 2025, Google indiquait une médiane de 0,24 Wh pour une requête texte) "
            "et sur la quantité de texte que cette application envoie et reçoit. La valeur réelle se situe "
            "probablement entre 0,5 et 2 Wh. Pour un CV scanné ou un JPG, la reconnaissance de texte "
            "s'ajoute : comptez environ le double."
        ),
        # upload
        "upload_header": "### Télécharger votre CV",
        "upload_caption": "Formats acceptés : PDF, Word (.docx) et JPG — 10 Mo maximum",
        "upload_scan_note": (
            "📄 **Un PDF donne le meilleur résultat** : nous pouvons y indiquer les erreurs directement.\n\n"
            "📷 **Un JPG est accepté, mais uniquement comme scan de votre CV** — pas une photo où l'on voit "
            "aussi votre table, vos mains ou l'arrière-plan. Veillez à ce que la feuille soit droite et nette."
        ),
        "upload_scan_warning": (
            "Vous avez téléchargé une image. Vérifiez qu'il s'agit d'un scan droit et net **du CV uniquement**. "
            "Attention : sur une image, nous ne pouvons pas encadrer les erreurs — elles figurent bien dans la liste."
        ),
        "upload_label": "Choisir votre CV",
        "upload_help": "Faites glisser votre CV ici ou cliquez pour choisir un fichier.",
        "upload_error_size": "Le fichier est trop volumineux ({size:.1f} Mo). La taille maximale est de {max} Mo.",
        "upload_error_type": "Le type de fichier '.{ext}' n'est pas pris en charge. Téléchargez un PDF, un fichier Word (.docx) ou un scan en JPG.",
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
        "results_no_improvements": "Aucun point d'amélioration trouvé — tout est en ordre selon la checklist !",
        # CV-preview
        "results_preview_header": "### Aperçu du CV",
        "results_preview_text_note": "Aperçu basé sur le texte extrait — la mise en page originale peut différer.",
        "results_preview_image_note": "Sur un scan ou une photo, nous ne pouvons pas placer de cadres. Le texte reconnu, avec les marquages, figure ci-dessous.",
        "results_preview_unavailable": "Aucun aperçu disponible pour ce fichier.",
        "results_see_marker": "📍 Voir le cadre {n} sur l'aperçu du CV à droite",
        # criteria checklist
        "results_checklist": "### Tous les critères évalués (la checklist CV)",
        "results_checklist_caption": (
            "Ce sont exactement les critères de la checklist CV papier — il n'y a pas de critères cachés. "
            "Si vous mettez tout en ordre selon la checklist et téléchargez à nouveau votre CV, vous obtenez 100/100."
        ),
        "checklist_complete": "entièrement en ordre",
        "checklist_met": "Entièrement présent",
        "checklist_partial": "Partiellement présent",
        "checklist_not_met": "Absent",
        "checklist_points": "points",
        "checklist_manual": "à vérifier visuellement soi-même",
        # address check
        "results_adres_header": "### Vérification de l'adresse",
        "adres_none": "Aucune adresse n'a été trouvée dans le CV.",
        "adres_ok": "L'adresse ({adres}) est écrite dans la même langue que le CV. ✓",
        "adres_mismatch": "Attention : l'adresse ({adres}) ne semble pas être écrite dans la même langue que le reste du CV.",
        # score labels
        "score_needs_work": "À améliorer",
        "score_sufficient": "Suffisant",
        "score_good": "Bien",
        "score_very_good": "Très bien",
        "score_excellent": "Excellent",
        "score_unknown": "Inconnu",
        # category names
        "cat_lay_out": "Mise en page",
        "cat_inhoud": "Contenu",
        "cat_structuur_opmaak": "Structure & Mise en page",
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
        "criteria_expander": "🛠️ Modifier les critères ou ajouter vos propres critères (pour les formateurs)",
        "criteria_caption": (
            "Vous pouvez activer ou désactiver des critères, modifier les descriptions et ajouter "
            "vos propres critères par catégorie pour cette session. "
            "Les modifications ne sont **pas enregistrées** et disparaissent lors du rechargement de la page."
        ),
        "criteria_new_label": "Nouveau critère",
        "criteria_new_placeholder": "Décrivez votre propre critère et cliquez sur « Ajouter »…",
        "criteria_new_btn": "➕ Ajouter",
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
        "ocr_info": "This CV was a scan or an image and could not be read directly. The text was recognised using AI (OCR) — the analysis is normally usable, but may be less accurate if the scan is blurry.",
        # privacy
        "privacy_short": "🔒 **Your CV is not stored.** There is no database and no account. As soon as you close the tab, everything is gone.",
        "privacy_header": "🔒 What exactly happens to my data?",
        "privacy_body": (
            "- **Your file is not saved.** It is briefly written to a temporary file to extract the text, "
            "and deleted immediately afterwards.\n"
            "- **There is no database, no account and no log** containing your data. "
            "Nobody — not even your trainer — can retrieve your CV afterwards.\n"
            "- The text of your CV is sent over a secure connection to the Anthropic API to produce the "
            "analysis. **Anthropic does not use this text to train AI models.**\n"
            "- As long as you keep this window open, your result stays in the server's memory. "
            "That is what makes you get exactly the same score if you re-upload the same CV. "
            "It expires automatically after at most 2 hours, or as soon as you click “Analyse a new CV”.\n"
            "- **Close the tab and everything is gone.**"
        ),
        # energy & CO2
        "impact_header": "🌱 How much energy does one analysis cost?",
        "impact_body": (
            "Analysing one CV costs an estimated **{wh} Wh** ({kwh} kWh) and **{co2} g CO₂**.\n\n"
            "That is roughly the same as:\n"
            "- a **kettle** boiling for {koker} seconds\n"
            "- an **LED lamp** burning for {lamp} minutes\n"
            "- {telefoon} analyses ≈ one full **smartphone charge**\n"
            "- the CO₂ of driving **{auto} metres** by car"
        ),
        "impact_note": (
            "Rough estimate, not a measurement. Based on publicly reported figures "
            "(in August 2025 Google reported a median of 0.24 Wh for a single text prompt) "
            "and on the amount of text this app sends and receives. The real value is probably "
            "between 0.5 and 2 Wh. For a scanned CV or a JPG, text recognition is added: "
            "expect roughly double."
        ),
        # upload
        "upload_header": "### Upload your CV",
        "upload_caption": "Supported formats: PDF, Word (.docx) and JPG — maximum 10 MB",
        "upload_scan_note": (
            "📄 **A PDF gives the best result**: we can mark the mistakes directly on it.\n\n"
            "📷 **A JPG is allowed too, but only as a scan of your CV** — not a photo that also shows your "
            "table, your hands or the background. Make sure the sheet is straight and sharp."
        ),
        "upload_scan_warning": (
            "You uploaded an image. Check that this is a straight, sharp scan of **the CV only**. "
            "Note: on an image we cannot mark the mistakes with boxes — you will still get them in the list."
        ),
        "upload_label": "Choose your CV",
        "upload_help": "Drag your CV here or click to choose a file.",
        "upload_error_size": "The file is too large ({size:.1f} MB). Maximum file size is {max} MB.",
        "upload_error_type": "File type '.{ext}' is not supported. Upload a PDF, a Word file (.docx) or a scan in JPG.",
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
        "results_no_improvements": "No improvement points found — everything on the checklist is in order!",
        # CV-preview
        "results_preview_header": "### CV preview",
        "results_preview_text_note": "Preview based on the extracted text — the original layout may differ.",
        "results_preview_image_note": "On a scan or photo we cannot place boxes. The recognised text, with the markings, is shown below.",
        "results_preview_unavailable": "No preview available for this file.",
        "results_see_marker": "📍 See box {n} on the CV preview on the right",
        # criteria checklist
        "results_checklist": "### All assessed criteria (the CV checklist)",
        "results_checklist_caption": (
            "These are exactly the criteria from the paper CV checklist — there are no hidden criteria. "
            "If you fix everything on the checklist and re-upload your CV, you score 100/100."
        ),
        "checklist_complete": "fully met",
        "checklist_met": "Fully present",
        "checklist_partial": "Partially present",
        "checklist_not_met": "Not present",
        "checklist_points": "points",
        "checklist_manual": "check visually yourself",
        # address check
        "results_adres_header": "### Address check",
        "adres_none": "No address was found in the CV.",
        "adres_ok": "The address ({adres}) is written in the same language as the CV. ✓",
        "adres_mismatch": "Note: the address ({adres}) does not appear to be written in the same language as the rest of the CV.",
        # score labels
        "score_needs_work": "Needs work",
        "score_sufficient": "Sufficient",
        "score_good": "Good",
        "score_very_good": "Very good",
        "score_excellent": "Excellent",
        "score_unknown": "Unknown",
        # category names
        "cat_lay_out": "Layout",
        "cat_inhoud": "Content",
        "cat_structuur_opmaak": "Structure & Layout",
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
        "criteria_expander": "🛠️ Adjust criteria or add your own criteria (for trainers)",
        "criteria_caption": (
            "You can enable or disable criteria, edit descriptions and add your own criteria "
            "per category for this session. "
            "Changes are **not saved** and disappear when the page is refreshed."
        ),
        "criteria_new_label": "New criterion",
        "criteria_new_placeholder": "Describe your own criterion and click 'Add'…",
        "criteria_new_btn": "➕ Add",
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
