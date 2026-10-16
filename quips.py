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
    "The heat death of the universe is proceeding ahead of schedule.",
    "Hydrate or die-drate.",
    "Vultures cool off by peeing on themselves.",
    "Climate Control has been transferred to a higher plane of existence.",
    "Hell has contacted us regarding a possible breach in contract.",
    "Hope you don't have leather car seats.",
    "The sun is actively trying to kill you.",
    "Even the AC is sweating.",
    "You could fry an egg on the sidewalk. Don't.",
    "Hell is leaving bad reviews about the heat.",
    "Today's weather has been brought to you by Climate Change.",
    "Don't check the power bill.",
    "The apocalypse was supposed to be more exciting than this.",
    "Congratulations. The planet has become a rotisserie.",
    "To Do: Boost Earth's magnetosphere.",
    "The Sun has been left unsupervised.",
    "Lizards rejoice!",
    "NASA would like to remind you that the Sun is not, in fact, getting closer.",
    "If you pass out, try not to hit your head.",
    "I just saw a pigeon lie down in the street and accept it.",
    "The devil turned on his space heater out of spite.",
    "Just don't even bother.",
    "Skin is temporary. The Sun, however, is longer lived.",
    "The sun is being controlled by raccoons.",
    "You wanted a big truck. This is what you get.",
    "You're the one that decided to be carbon-based.",
    "We hung the jerk that invented the Greenhouse Effect.",
    "The pavement has become a skillet.",
    "Double Black Flag is in effect. Wait until you see Triple Black Flag.",
    "Fun fact: You are mostly water, and the sky is trying to remove it.",
    "We have mandated a formal inquiry.",
]

QUIPS_TEMP_HIGH = [
    "Turn on a fan or something.",
    "At least open a window.",
    "Don't leave chocolate in the car.",
    "Wear some deodorant, everyone will thank you.",
    "Sunscreen prevents skin cancer.",
    "Shorts weather, no excuses.",
    "The local star is operating within specifications.",
    "Find shade like it owes you money.",
    "Park in the shade. Future you will thank you.",
    "Who touched the thermostat?",
    "It's hot.",
    "The Sun woke up and chose violence.",
    "A lovely day to test your deodorant's limitations.",
    "Your plans are subject to a giant ball of plasma.",
    "The atmosphere has resumed hostilities.",
    "This is just a preview.",
    "The weather is lovely if you're a lizard.",
    "Beach weather.",
    "We would like to remind you that the Sun hates you.",
    "Horoscope: Someone close to you will smell your sweat. Disgusting.",
    "The Sun is working overtime.",
    "Humidity: nature's weighted blanket.",
    "Your shirt has filed a formal complaint.",
    "Don't worry. It gets worse.",
    "The mosquitoes have been waiting for you, specifically.",
    "Welcome to the rest of your life.",
    "You are developing an unhealthy relationship with air conditioning.",
    "Showers hurt no one.",
    "If this keeps up, the polar bears are going to invade.",
    "All outdoor plans have been moved to the ice box.",
    "Summer already? Damn.",
    "Temperature rises as pressure builds. Anyway, how's that essay coming along?",
    "The surface of the sun is roughly 10,000 degrees Fahrenheit. What a show off."
]

QUIPS_TEMP_NORMAL = [
    "The one day the app name doesn't apply",
    "Take a walk outside",
    "Go to the park",
    "Reduce, Reuse, Recycle",
    "Stay hydrated, hero!",
    "Period queen, slay!",
    "This temporary delay in heat-stroke is brought to you by mild weather.",
    "Perfect weather. Suspicious.",
    "Open the windows, save on the electric bill",
    "Touch some grass, it's nice out",
    "Fun fact: Venus can experience temperatures as high as 850°F due to a runaway Greenhouse Effect.",
    "The weather is behaving. An investigation is underway.",
    "Mercury goes from 800°F to -290°F daily. You live on the nice planet.",
    "Don't worry, today is just the control group.",
    "Go get some vitamin D.",
    "No notes. Deeply unsettling.",
    "Please enjoy this brief period of atmospheric cooperation.",
    "Conditions are acceptable. Don't get used to it.",
    "The planet has decided to be tolerable today.",
    "Scientists are baffled by today's lack of nonsense.",
    "Everything is fine. This is how they get you.",
    "The atmosphere has temporarily suspended hostilities.",
    "Weather like this almost makes you forget we're living on a giant rock hurtling through space.",
    "Take a moment to appreciate the cosmic coincidence that allows you to exist.",
    "The apocalypse can wait.",
    "Koalas hug trees to cool off. Find a tree. Hold it.",
    "The world isn't ending. Yet.",
    "The bottom layer of the Mesosphere is roughly -15°C. Too bad you're down here."
]

QUIPS_TEMP_LOW = [
    "Bring a jacket, champ.",
    "It's getting chilly.",
    "Hoodie season!",
    "Soup weather.",
    "Fun fact: You actually CAN drink too much water. Doesn't mean you should stop.",
    "Time for your special socks.",
    "Your mom called and said to wear layers.",
    "It may be cold, but still drink water.",
    "Steal a blanket from someone you love.",
    "Who touched the thermostat?!",
    "Hot drink in hand, dread in heart.",
    "Your skin is begging for some lotion.",
    "Can you smell the turkey and stuffing yet?",
    "The Sun sets at 6pm now. Nobody voted for this.",
    "The flies are dying. Small victories.",
    "Goosebumps: a fur feature you no longer have the fur for.",
    "Shivering is cardio you didn't sign up for.",
    "Fleece is just plastic bottles. You're wearing a recycling bin.",
    "Pumpkin spice has no actual pumpkin in it. Everything is a lie. Wear a jacket.",
    "Monarch butterflies fly 3,000 miles to Mexico for the winter. You won't even walk to the mailbox.",
    "Fun fact: Leaves don't turn orange; the green just hides it.",
    "Fun fact: Bears do not poop during hibernation.",
    "Fun fact: A chickadee's hippocampus expands by 30 percent in the fall to remember where it hid its snacks.",
    "Down jackets are made of duck underwear. Stay warm.",
    "Your sweater is a sheep's old haircut.",
    "Trees cut off their own leaves on purpose in the fall.",
    "Your Halloween pumpkin is rotting from the inside. So are we all.",
    "Squirrels forget where they bury most of their nuts. That's how forests happen. Your mistakes could be a forest.",
    "The best time to plant a tree was 20 years ago. The second best time is when it is warmer out.",
    "Stink bugs are moving into your walls for the winter. They don't pay rent.",
    "Ticks don't die when it gets cold. Just thought you should know.",
    "Farmers didn't invent daylight saving time. Farmers hated it. Nobody wanted this.",
    "The geese are leaving. They know something.",
    "Horoscope: You will wear shorts out of pride, and pride will lose.",
]

QUIPS_TEMP_V_LOW = [
    "Go scrape your windshield",
    "Your glasses will fog immediately",
    "Don't lick the flagpole",
    "Weather is just a game. You lose.",
    "Your car battery is scared",
    "Cold enough to freeze your nose hairs",
    "Hot cocoa is a food group now",
    "Dress like a burrito",
    "Check on your pipes",
    "Your tires lose about 1 PSI for every 10 degrees it drops.",
    "Good News: Your PC temps will be much better.",
    "Polar bears maintain a core body temperature of 36.9 °C in Arctic conditions. Too bad.",
    "Your toes have filed for divorce.",
    "Metal surfaces are now a war crime",
    "Your part of the planet is the furthest from the sun. Congratulations.",
    "Frostbite occurs within 30 minutes at 0°F. Wear loose, comfortable layers.",
    "Gloves were never optional.",
    "Your body actively pulls blood away from extremities to warm your organs. Cover up.",
    "Ötzi the Iceman froze 5,300 years ago and still has sick tattoos.",
    "Spring should come any minute now...",
    "Wood frogs freeze solid and thaw out alive. You are not a wood frog.",
    "Fun fact: The coldest temperature ever recorded on Earth was -128.6 °F. Quit whining.",
    "It could be worse, Uranus gets down to -224.2 °C.",
    "Tardigrades can survive almost absolute zero. You can't survive the walk to your car.",
    "Physics is actively working against you.",
    "The temperature is a personal attack against you.",
]

# ===== CONDITION QUIPS =====
# These replace temperature quips. Checked in order; the first keyword match wins.
QUIPS_CONDITION = {
    "hail": [
        "The sky is throwing ice at you.",
        "Hail can fall over 100 mph.",
        "Hail. No punchline. Please be careful.",
    ],
    "thunder": [
        "Thor is having a tantrum.",
        "Count the seconds, then hide.",
        "Ben Franklin flew a kite in a storm and lived; the next guy who tried it died. Stay inside.",
        "Thunderstorms shoot out gamma rays and antimatter.",
        "Somewhere, a guy holding a golf club is about to learn about conductivity.",
        "Did you hear that? The sky is trying to reach you.",
    ],
    "freezing": [
        "Black ice isn't black, it's clear. You can't see it. That's the whole problem.",
        "Ice can add hundreds of pounds to a single power line. Charge your phone.",
        "The roads are now a hockey rink with no rules.",
        "Going out for groceries is optional, today.",
    ],
    "snow": [
        "Drive like your grandma is watching.",
        "Shovel now, cry later.",
        "Hope you got your milk and bread.",
        "About a septillion snowflakes fall every winter. You'll shovel most of them.",
        "It snows on Mars, but it's frozen CO2.",
        "Thundersnow is real. The sky can do both at once. Be afraid.",
        "Snow absorbs sound.",
        "Every driver is now going either 10 mph or 90 mph.",
    ],
    "drizzle": [
        "Spitting rain, the worst kind.",
        "The rain should make up its mind.",
        "Just a little dribble.",
        "Not enough rain for an umbrella. Just enough to annoy you.",
        "The sky is the guy who spits a little when he talks.",
        "Your windshield wipers will squeak on every setting.",
    ],
    "rain": [
        "Grab an umbrella.",
        "Your hair is doomed.",
        "The fish are rising up, land dwellers beware.",
        "Puddle-jumping is legally encouraged.",
        "That rain smell is partly made by soil bacteria. Breathe deep.",    
        "Tell the coroner it was raining. See if he cares.",
        "Your shoes will make the squelch noise all day. Accept it.",
    ],
    "showers": [
        "Rain, then no rain, then rain. The sky can't make up its mind.",
        "Umbrellas have been around for thousands of years and they still flip inside out.",
        "It'll stop the second you get inside. Then start again when you leave.",
    ],
    "fog": [
        "The clouds are lying down.",
        "Low beams, not high beams.",
        "Beware: Do not enter the fog.",
        "You're inside a cloud right now. Technically that's heaven. Congrats, you died.",
        "Rime fog freezes onto everything it touches. Don't stand still too long.",
    ],
}

# ===== SKY QUIPS =====
# These get mixed in with the temperature quips instead of replacing them.
QUIPS_SKY = {
    "sunny": [
        "The deadly laser is out.",
        "The forecast is uneventful. We apologize for the lack of drama.",
        "Nothing to report. Reality continues.",
        "Enjoy the outdoors before the simulation notices.",
        "It's suspiciously calm.",
        "Fun fact: It would take 1.3 million Earths to fill the Sun's volume.",
        "Fun fact: The Sun orbits the Milky Way. One lap takes about 230 million years.",
        "The Sun is 4.6 billion years old and will become a red giant in roughly 4-5 billion more.",
        "Sunlight is 8 minutes old. You're staring at the past. Don't actually stare at it, though.",
    ],
    "clear": [
        "Clear nights get colder because there are no clouds to trap the heat.",
        "The Andromeda galaxy's light is 2.5 million years old.",
        "The Moon drifts about 1.5 inches farther away every year.",
        "Astronauts say moon dust smells like spent gunpowder.",
        "Voyager 1 is out there right now, alone, farther from home than anything we've ever made.",
        "The stars are out. They're judging you.",
    ],
    "cloudy": [
        "A regular puffy cloud weighs about a million pounds. It's floating right above you.",
        "Fear of clouds is called nephophobia. Today is a bad day for those guys.",
        "The Sun called in sick.",
    ],
}


def get_quip(temp_f: float, condition: str = "") -> str:
    """
    Pick a random quip for the current weather.

    Weather events like rain or snow take priority over temperature, since they matter more
    for what to wear. Sky quips (sunny, clear, cloudy) get mixed in with the temperature quips
    instead. Temperatures are always in °F, so the quip doesn't change when the display
    switches to Celsius.

    Args:
        temp_f: Current temperature in °F.
        condition: Current weather description, e.g. "Light Rain". Matched case-insensitively.

    Returns:
        str: A randomly chosen quip.
    """
    condition = condition.lower()
    for keyword, quips in QUIPS_CONDITION.items():
        if keyword in condition:
            return random.choice(quips)

    if temp_f >= V_HIGH_F:
        pool = QUIPS_TEMP_V_HIGH
    elif temp_f >= HIGH_F:
        pool = QUIPS_TEMP_HIGH
    elif temp_f >= NORMAL_F:
        pool = QUIPS_TEMP_NORMAL
    elif temp_f >= LOW_F:
        pool = QUIPS_TEMP_LOW
    else:
        pool = QUIPS_TEMP_V_LOW

    for keyword, quips in QUIPS_SKY.items():
        if keyword in condition:
            pool = pool + quips
            break

    return random.choice(pool)
