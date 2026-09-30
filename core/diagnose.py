#!/usr/bin/env python3
"""Zelfdiagnose van de verbinding met de Anthropic-API.

Bedoeld voor de begeleider: bij een fout rond tegoed of toegang is de vraag
altijd dezelfde — ligt het aan de sleutel of aan het tegoed? Dit onderscheid
maak je door de modellenlijst op te vragen: die aanroep kost geen tokens en
wordt dus niet geweigerd wegens een leeg tegoed.

    sleutel geweigerd (401/403)  -> de sleutel is fout, verlopen of ingetrokken
    sleutel aanvaard, analyse    -> de sleutel klopt; het tegoed of de
    faalt op tegoed                 uitgavenlimiet van díé organisatie is op

Er wordt nooit (een deel van) de sleutel zelf getoond.
"""

import os


def _sleutel_regel() -> str:
    sleutel = os.environ.get("ANTHROPIC_API_KEY", "")
    if not sleutel:
        return "❌ Er is geen API-sleutel ingesteld (ANTHROPIC_API_KEY ontbreekt)."
    vorm = "sk-ant-" if sleutel.startswith("sk-ant-") else "onbekend"
    regel = f"• Er is een sleutel ingesteld ({len(sleutel)} tekens, vorm: {vorm})."
    if vorm == "onbekend":
        regel += " ⚠️ Dit lijkt geen geldige Anthropic-sleutel."
    if sleutel != sleutel.strip():
        regel += " ⚠️ Er staat een spatie of regeleinde omheen — haal die weg."
    return regel


def diagnose_api() -> list[str]:
    """Controleer sleutel en tegoed. Geeft leesbare regels terug."""
    regels = [_sleutel_regel()]

    sleutel = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not sleutel:
        regels.append("Zet de sleutel bij de secrets van de app en herstart hem.")
        return regels

    try:
        import anthropic
    except ImportError:
        regels.append("• De anthropic-bibliotheek is niet geïnstalleerd.")
        return regels

    # De modellenlijst kost geen tokens: slaagt dit, dan is de sleutel geldig
    # en gaat het dus zuiver om het tegoed of een uitgavenlimiet.
    try:
        anthropic.Anthropic(api_key=sleutel).models.list(limit=1)
    except anthropic.AuthenticationError:
        regels.append(
            "❌ De API wijst deze sleutel af (401). De sleutel is fout, verlopen of "
            "ingetrokken. Maak een nieuwe aan in de Anthropic Console en vervang hem "
            "bij de secrets van de app."
        )
        return regels
    except anthropic.PermissionDeniedError:
        regels.append(
            "❌ Deze sleutel heeft geen toegang (403). Controleer of de sleutel bij de "
            "juiste workspace hoort en of die workspace niet uitgeschakeld is."
        )
        return regels
    except anthropic.APIConnectionError:
        regels.append("• Geen verbinding met de API — controleer het netwerk.")
        return regels
    except Exception as fout:
        regels.append(f"• Onverwacht antwoord bij de controle: {fout}")
        return regels

    regels.append(
        "✅ De sleutel wordt aanvaard door de API — de sleutel zelf is dus in orde."
    )
    regels.append(
        "➡️ De fout gaat dan zuiver over tegoed: de organisatie of workspace waar "
        "DEZE sleutel bij hoort, heeft geen bruikbaar tegoed. Let op de drie "
        "klassiekers:"
    )
    regels.append(
        "   1. Een Claude Pro/Max-abonnement telt NIET als API-tegoed. API-tegoed "
        "koop je apart in de Anthropic Console bij Plans & Billing."
    )
    regels.append(
        "   2. Het tegoed is opgeladen in een andere organisatie dan waar deze "
        "sleutel bij hoort (bv. een persoonlijk account naast een werkaccount)."
    )
    regels.append(
        "   3. De workspace van deze sleutel heeft een eigen uitgavenlimiet die op "
        "nul staat of bereikt is (Console → Settings → Workspaces → Spend limit)."
    )
    return regels
