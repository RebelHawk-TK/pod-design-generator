"""Video generator constants, landmark/style data, and timing config."""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
FONTS_DIR = BASE_DIR / "fonts"
OUTPUT_DIR = BASE_DIR / "output" / "videos"
AUDIO_CACHE_DIR = OUTPUT_DIR / ".audio_cache"
POSTER_SOURCE_DIR = (
    BASE_DIR.parent / "landmark-style-transfer" / "output" / "poster"
)

# ---------------------------------------------------------------------------
# Video dimensions & encoding
# ---------------------------------------------------------------------------

WIDTH = 1080
HEIGHT = 1920
FPS = 30
CODEC = "libx264"
AUDIO_CODEC = "aac"

# Working resolution for Ken Burns (downscaled from 3840)
WORK_RES = 2160

# ---------------------------------------------------------------------------
# Timing (seconds)
# ---------------------------------------------------------------------------

INTRO_DURATION = 2.0
CLIP_DURATION = 8.0
OUTRO_DURATION = 5.0
CROSSFADE = 0.5
VOICEOVER_START = 2.0  # VO begins after intro

# Total ≈ 2 + 8 + 5 - 2*(0.5) = 14s
CLIPS_PER_VIDEO = 1

# ---------------------------------------------------------------------------
# TTS config
# ---------------------------------------------------------------------------

TTS_VOICE = "en-US-GuyNeural"
TTS_RATE = "+5%"

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------

TITLE_FONT = FONTS_DIR / "BebasNeue-Regular.ttf"
BODY_FONT = FONTS_DIR / "PatrickHand-Regular.ttf"

# ---------------------------------------------------------------------------
# Default style triplet for videos
# ---------------------------------------------------------------------------

DEFAULT_STYLE_TRIPLET = ["starry_night", "great_wave", "water_lilies"]

# ---------------------------------------------------------------------------
# Landmarks (25 entries)
# ---------------------------------------------------------------------------

LANDMARKS = {
    "eiffel_tower": {
        "display_name": "Eiffel Tower",
        "location": "Paris, France",
        "tagline": "iron icon of romance and revolution",
    },
    "taj_mahal": {
        "display_name": "Taj Mahal",
        "location": "Agra, India",
        "tagline": "marble monument to eternal love",
    },
    "colosseum": {
        "display_name": "Colosseum",
        "location": "Rome, Italy",
        "tagline": "ancient arena of gladiators and glory",
    },
    "great_wall": {
        "display_name": "Great Wall",
        "location": "China",
        "tagline": "stone serpent stretching across mountains",
    },
    "notre_dame": {
        "display_name": "Notre-Dame",
        "location": "Paris, France",
        "tagline": "gothic masterpiece on the Seine",
    },
    "neuschwanstein": {
        "display_name": "Neuschwanstein Castle",
        "location": "Bavaria, Germany",
        "tagline": "fairy-tale castle in the clouds",
    },
    "mount_fuji": {
        "display_name": "Mount Fuji",
        "location": "Honshu, Japan",
        "tagline": "sacred peak of snow and symmetry",
    },
    "golden_gate": {
        "display_name": "Golden Gate Bridge",
        "location": "San Francisco, USA",
        "tagline": "art-deco span across the fog",
    },
    "sydney_opera": {
        "display_name": "Sydney Opera House",
        "location": "Sydney, Australia",
        "tagline": "sculptural sails on the harbour",
    },
    "santorini": {
        "display_name": "Santorini",
        "location": "Cyclades, Greece",
        "tagline": "white-washed cliffs above the Aegean",
    },
    "angkor_wat": {
        "display_name": "Angkor Wat",
        "location": "Siem Reap, Cambodia",
        "tagline": "temple of towers rising from the jungle",
    },
    "machu_picchu": {
        "display_name": "Machu Picchu",
        "location": "Cusco, Peru",
        "tagline": "lost city above the clouds",
    },
    "sagrada_familia": {
        "display_name": "Sagrada Familia",
        "location": "Barcelona, Spain",
        "tagline": "Gaudí's unfinished symphony in stone",
    },
    "parthenon": {
        "display_name": "Parthenon",
        "location": "Athens, Greece",
        "tagline": "crown of the Acropolis",
    },
    "stonehenge": {
        "display_name": "Stonehenge",
        "location": "Wiltshire, England",
        "tagline": "ancient circle of mystery and alignment",
    },
    "moai": {
        "display_name": "Moai Statues",
        "location": "Easter Island, Chile",
        "tagline": "stone guardians watching the Pacific",
    },
    "pyramids_giza": {
        "display_name": "Pyramids of Giza",
        "location": "Giza, Egypt",
        "tagline": "timeless tombs beneath the desert sun",
    },
    "petra": {
        "display_name": "Petra",
        "location": "Ma'an, Jordan",
        "tagline": "rose-red city carved from canyon walls",
    },
    "st_basils": {
        "display_name": "St. Basil's Cathedral",
        "location": "Moscow, Russia",
        "tagline": "candy-colored domes on Red Square",
    },
    "chichen_itza": {
        "display_name": "Chichén Itzá",
        "location": "Yucatán, Mexico",
        "tagline": "pyramid of the feathered serpent",
    },
    "christ_redeemer": {
        "display_name": "Christ the Redeemer",
        "location": "Rio de Janeiro, Brazil",
        "tagline": "open arms above the city of samba",
    },
    "hagia_sophia": {
        "display_name": "Hagia Sophia",
        "location": "Istanbul, Turkey",
        "tagline": "where empires meet beneath the dome",
    },
    "tower_of_pisa": {
        "display_name": "Tower of Pisa",
        "location": "Pisa, Italy",
        "tagline": "the world's most charming mistake",
    },
    "big_ben": {
        "display_name": "Big Ben",
        "location": "London, England",
        "tagline": "clocktower keeping time for a nation",
    },
    "statue_of_liberty": {
        "display_name": "Statue of Liberty",
        "location": "New York, USA",
        "tagline": "copper beacon of freedom and hope",
    },
    # ----- Phase 2 Landmarks -----
    "amsterdam_canals": {
        "display_name": "Amsterdam Canal Ring",
        "location": "Amsterdam, Netherlands",
        "tagline": "golden age waterways framed by gabled houses",
    },
    "bagan_temples": {
        "display_name": "Bagan Temple Plain",
        "location": "Bagan, Myanmar",
        "tagline": "thousands of temples across a misty plain",
    },
    "bruges_medieval": {
        "display_name": "Bruges Medieval Center",
        "location": "Bruges, Belgium",
        "tagline": "fairy-tale canals of medieval Flanders",
    },
    "charles_bridge": {
        "display_name": "Charles Bridge",
        "location": "Prague, Czech Republic",
        "tagline": "gothic arches spanning the Vltava at dawn",
    },
    "chefchaouen": {
        "display_name": "Chefchaouen",
        "location": "Chefchaouen, Morocco",
        "tagline": "blue-painted streets in the Rif Mountains",
    },
    "edinburgh_old_town": {
        "display_name": "Edinburgh Old Town",
        "location": "Edinburgh, Scotland",
        "tagline": "medieval wynds beneath castle rock",
    },
    "fushimi_inari": {
        "display_name": "Fushimi Inari Shrine",
        "location": "Kyoto, Japan",
        "tagline": "ten thousand vermilion gates climbing the mountain",
    },
    "giants_causeway": {
        "display_name": "Giant's Causeway",
        "location": "County Antrim, Northern Ireland",
        "tagline": "hexagonal basalt columns born of legend and lava",
    },
    "guanajuato": {
        "display_name": "Guanajuato",
        "location": "Guanajuato, Mexico",
        "tagline": "rainbow hillside city of silver and song",
    },
    "hallgrimskirkja": {
        "display_name": "Hallgrímskirkja",
        "location": "Reykjavík, Iceland",
        "tagline": "basalt-inspired spire above the northern capital",
    },
    "hapenny_bridge": {
        "display_name": "Ha'penny Bridge",
        "location": "Dublin, Ireland",
        "tagline": "elegant iron arch over the River Liffey",
    },
    "havana_vieja": {
        "display_name": "Old Havana",
        "location": "Havana, Cuba",
        "tagline": "pastel facades and vintage charm on the Caribbean",
    },
    "hawa_mahal": {
        "display_name": "Hawa Mahal",
        "location": "Jaipur, India",
        "tagline": "honeycomb palace of nine hundred fifty-three windows",
    },
    "hoi_an": {
        "display_name": "Hoi An Ancient Town",
        "location": "Hoi An, Vietnam",
        "tagline": "lantern-lit streets beside the Thu Bon River",
    },
    "milford_sound": {
        "display_name": "Milford Sound",
        "location": "Fiordland, New Zealand",
        "tagline": "towering fjord walls veiled in mist and waterfalls",
    },
    "mont_saint_michel": {
        "display_name": "Mont Saint-Michel",
        "location": "Normandy, France",
        "tagline": "medieval abbey rising from the tidal flats",
    },
    "moraine_lake": {
        "display_name": "Moraine Lake",
        "location": "Banff, Canada",
        "tagline": "turquoise jewel cradled by the Valley of the Ten Peaks",
    },
    "nyhavn": {
        "display_name": "Nyhavn",
        "location": "Copenhagen, Denmark",
        "tagline": "colorful harbour houses along the old sailor's port",
    },
    "plitvice_lakes": {
        "display_name": "Plitvice Lakes",
        "location": "Plitvice, Croatia",
        "tagline": "cascading turquoise lakes in an ancient forest",
    },
    "ponte_vecchio": {
        "display_name": "Ponte Vecchio",
        "location": "Florence, Italy",
        "tagline": "medieval bridge of goldsmiths above the Arno",
    },
    "rialto_bridge": {
        "display_name": "Rialto Bridge",
        "location": "Venice, Italy",
        "tagline": "marble arch crowning the Grand Canal",
    },
    "rijksmuseum": {
        "display_name": "Rijksmuseum",
        "location": "Amsterdam, Netherlands",
        "tagline": "cathedral of Dutch masters and golden age glory",
    },
    "temple_bar": {
        "display_name": "Temple Bar",
        "location": "Dublin, Ireland",
        "tagline": "cobblestoned heart of Dublin's cultural quarter",
    },
    "twelve_apostles": {
        "display_name": "Twelve Apostles",
        "location": "Great Ocean Road, Australia",
        "tagline": "limestone sentinels sculpted by the Southern Ocean",
    },
    "zanzibar_stone_town": {
        "display_name": "Zanzibar Stone Town",
        "location": "Zanzibar, Tanzania",
        "tagline": "carved doors and spice-scented alleys on the Indian Ocean",
    },
}

# ---------------------------------------------------------------------------
# Art styles (6 entries)
# ---------------------------------------------------------------------------

STYLES = {
    "starry_night": {
        "display_name": "Starry Night",
        "artist": "Vincent van Gogh",
        "movement": "Post-Impressionism",
    },
    "great_wave": {
        "display_name": "The Great Wave",
        "artist": "Katsushika Hokusai",
        "movement": "Ukiyo-e",
    },
    "water_lilies": {
        "display_name": "Water Lilies",
        "artist": "Claude Monet",
        "movement": "Impressionism",
    },
    "the_scream": {
        "display_name": "The Scream",
        "artist": "Edvard Munch",
        "movement": "Expressionism",
    },
    "cafe_terrace": {
        "display_name": "Café Terrace at Night",
        "artist": "Vincent van Gogh",
        "movement": "Post-Impressionism",
    },
    "composition_vii": {
        "display_name": "Composition VII",
        "artist": "Wassily Kandinsky",
        "movement": "Abstract Expressionism",
    },
}
