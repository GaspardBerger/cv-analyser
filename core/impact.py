#!/usr/bin/env python3
"""Schatting van het energieverbruik en de CO2-uitstoot van één CV-analyse.

Alle getallen hieronder zijn een ORDE-VAN-GROOTTE-SCHATTING, geen meting.
Aanbieders van AI-modellen publiceren geen verbruik per afzonderlijke oproep,
dus we rekenen met publiek gerapporteerde referentiewaarden en met wat deze
app effectief verstuurt en ontvangt.

Redenering:

1. Omvang van één analyse
   - invoer:  systeemprompt met alle criteria (~1.800 tokens) + de CV-tekst
              (~800–1.500 tokens)  ->  afgerond ~3.000 tokens
   - uitvoer: beoordeling van elk criterium met toelichting, plus de
              verbeterpunten met voorbeeld  ->  ~1.500–3.000 tokens
   Het genereren van uitvoer weegt veruit het zwaarst in het verbruik.

2. Energie per oproep
   Google rapporteerde in augustus 2025 een mediaan van 0,24 Wh voor één
   tekstprompt bij Gemini (inclusief datacenteroverhead). Zo'n mediaanprompt
   levert een kort antwoord op; onze analyse genereert een veelvoud daarvan.
   Met een factor 3 à 8 komen we op ongeveer 0,5–2 Wh per analyse.
   We rekenen verder met 1 Wh als centrale schatting.

3. CO2
   Datacenters van grote aanbieders draaien op een mix met veel hernieuwbare
   energie; gerapporteerde waarden liggen rond 100–250 g CO2 per kWh.
   We rekenen met 200 g/kWh.

Bij een gescand CV (PDF-scan of JPG) komt er tekstherkenning bij: dat is een
extra oproep met een afbeelding, goed voor ongeveer een verdubbeling. Staat er
een pasfoto in de PDF, dan komt daar nog een kleine beeldoproep bij; die is
klein genoeg om binnen de marge van deze schatting te vallen.
"""

# ── Aannames (pas hier aan als er betere cijfers beschikbaar zijn) ───────────

ENERGIE_ANALYSE_WH = 1.0        # centrale schatting per CV-analyse
ENERGIE_ONDERGRENS_WH = 0.5
ENERGIE_BOVENGRENS_WH = 2.0
ENERGIE_OCR_WH = 1.0            # extra bij een scan/foto (tekstherkenning)
CO2_PER_KWH_G = 200.0           # gemiddelde datacentermix

# Vergelijkingsmateriaal: vermogen van huishoudtoestellen in watt
WATERKOKER_W = 2000
LEDLAMP_W = 8
SMARTPHONE_ACCU_WH = 12         # volledige lading van een gemiddelde smartphone
AUTO_CO2_PER_KM_G = 120         # gemiddelde personenwagen


def co2_gram(energie_wh: float) -> float:
    """CO2-uitstoot (gram) voor een gegeven energieverbruik in wattuur."""
    return energie_wh / 1000.0 * CO2_PER_KWH_G


def schatting(met_ocr: bool = False) -> dict:
    """Geef de schatting voor één analyse, met vergelijkingen.

    met_ocr=True voor een gescand CV (PDF-scan of JPG), waarbij er ook
    tekstherkenning nodig is.
    """
    energie_wh = ENERGIE_ANALYSE_WH + (ENERGIE_OCR_WH if met_ocr else 0.0)
    return {
        "energie_wh": energie_wh,
        "energie_kwh": energie_wh / 1000.0,
        "ondergrens_wh": ENERGIE_ONDERGRENS_WH,
        "bovengrens_wh": ENERGIE_BOVENGRENS_WH,
        "co2_g": co2_gram(energie_wh),
        # Vergelijkingen met huishoudtoestellen
        "waterkoker_s": energie_wh * 3600.0 / WATERKOKER_W,
        "ledlamp_min": energie_wh * 60.0 / LEDLAMP_W,
        "smartphone_aantal": SMARTPHONE_ACCU_WH / energie_wh,
        "auto_m": co2_gram(energie_wh) / AUTO_CO2_PER_KM_G * 1000.0,
    }


def nl_getal(waarde: float, decimalen: int = 1) -> str:
    """Formatteer een getal met een komma als decimaalteken."""
    return f"{waarde:.{decimalen}f}".replace(".", ",")
