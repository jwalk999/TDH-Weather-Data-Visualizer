"""
File Name: quips.py

Author: Jonathan W
Date Created: 10/7/2026
Last Update: 10/7/2026
Version: 0.0.1

Scope: Picks a random quip based on the current temperature and weather conditions
"""

import random

# ===== THRESHOLDS (°F) =====
# A temperature at or above a threshold falls in that bucket; anything below LOW_F is very low.
V_HIGH_F = 95
HIGH_F = 80
NORMAL_F = 65
LOW_F = 40

# ===== TEMPERATURE QUIPS =====
QUIPS_TEMP_V_HIGH = [
    "It's too damn hot!",
    "It's hotter than Satan's asshole!",
    "It's hotter than a whore in church!",
    "Satan called: It's too damn hot!",
    "Hydrate or die-drate",
    "Hope you don't have leather carseats",
    "The sun is actively trying to kill you",
    "Even the AC is sweating",
    "You could fry an egg on the sidewalk. Don't.",
    "Hell is leaving bad reviews about the heat",
]

QUIPS_TEMP_HIGH = [
    "Turn on a fan or something",
    "At least open a window",
    "Don't leave chocolate in the car",
    "Wear some deodorant, everyone will thank you",
    "Sunscreen prevents skin cancer",
    "Shorts weather, no excuses",
    "Iced coffee is now mandatory",
    "Find shade like it owes you money",
    "Park in the shade, future you says thanks",
]

QUIPS_TEMP_NORMAL = [
    "The one day the app's name does not apply",
    "Take a walk outside",
    "Go to the park",
    "Reduce, Reuse, Recycle",
    "Drink lots of water",
    "Period queen, slay!",
    "Perfect weather. Suspicious.",
    "Open the windows, save on the electric bill",
    "Touch some grass, it's nice out",
]

QUIPS_TEMP_LOW = [
    "Bring a jacket, champ",
    "It's getting chilly",
    "Hoodie season!",
    "Your mom called and said to wear layers",
    "Time for your special socks",
    "It may be cold, but still drink water",
    "Soup weather, officially",
    "Steal a blanket from someone you love",
]

QUIPS_TEMP_V_LOW = [
    "Go scrape your windshield",
    "Your glasses will fog immediately",
    "Don't lick the flagpole",
    "Your car battery is scared",
    "Cold enough to freeze your nose hairs",
    "Hot cocoa is a food group now",
    "Dress like a burrito",
    "Check on your pipes",
]

# ===== CONDITION QUIPS =====
# Checked against the weather description in order; the first keyword match wins.
QUIPS_CONDITION = {
    "thunder": [
        "Thor is having a tantrum",
        "Unplug the nice electronics",
        "Count the seconds, then hide",
    ],
    "snow": [
        "Drive like your grandma is watching",
        "Shovel now, cry later",
    ],
    "rain": [
        "Grab an umbrella",
        "Your hair is doomed",
        "The fish are rising up, land dwellers beware",
        "Puddle-jumping is legally encouraged",
    ],
    "drizzle": [
        "Spitting rain, the worst kind",
        "Not enough rain for an umbrella. Just enough to annoy you.",
    ],
    "fog": [
        "Silent Hill vibes",
        "Low beams, not high beams",
        "Beware: Do not enter the fog",
    ],
}


def get_quip(temp_f: float, condition: str = "") -> str:
    """
    Pick a random quip for the current weather.

    Weather conditions like rain or snow take priority over temperature, since they matter
    more for what to wear. Temperatures are always in °F, so the quip doesn't change when
    the display switches to Celsius.

    Args:
        temp_f: Current temperature in °F.
        condition: Current weather description, e.g. "Light rain". Matched case-insensitively
            against the keys of ``QUIPS_CONDITION``.

    Returns:
        str: A randomly chosen quip.
    """
    condition = condition.lower()
    for keyword, quips in QUIPS_CONDITION.items():
        if keyword in condition:
            return random.choice(quips)

    if temp_f >= V_HIGH_F:
        quip_display = random.choice(QUIPS_TEMP_V_HIGH)
    elif temp_f >= HIGH_F:
        quip_display = random.choice(QUIPS_TEMP_HIGH)
    elif temp_f >= NORMAL_F:
        quip_display = random.choice(QUIPS_TEMP_NORMAL)
    elif temp_f >= LOW_F:
        quip_display = random.choice(QUIPS_TEMP_LOW)
    else:
        quip_display = random.choice(QUIPS_TEMP_V_LOW)

    return quip_display