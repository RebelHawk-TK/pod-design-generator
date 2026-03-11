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
    # ----- Phase 3 Landmarks -----
    "table_mountain": {
        "display_name": "Table Mountain",
        "location": "Cape Town, South Africa",
        "tagline": "flat-topped sentinel above two oceans",
    },
    "victoria_falls": {
        "display_name": "Victoria Falls",
        "location": "Zambia/Zimbabwe",
        "tagline": "the smoke that thunders across the Zambezi",
    },
    "djemaa_el_fna": {
        "display_name": "Djemaa el-Fna",
        "location": "Marrakech, Morocco",
        "tagline": "ancient square alive with storytellers and spice",
    },
    "lalibela_churches": {
        "display_name": "Rock-Hewn Churches of Lalibela",
        "location": "Lalibela, Ethiopia",
        "tagline": "sacred chambers carved from living rock",
    },
    "serengeti": {
        "display_name": "Serengeti",
        "location": "Tanzania",
        "tagline": "endless plains of the great migration",
    },
    "borobudur": {
        "display_name": "Borobudur Temple",
        "location": "Java, Indonesia",
        "tagline": "Buddhist pyramid rising through morning mist",
    },
    "terracotta_warriors": {
        "display_name": "Terracotta Warriors",
        "location": "Xi'an, China",
        "tagline": "an emperor's silent army guarding eternity",
    },
    "golden_temple_amritsar": {
        "display_name": "Golden Temple",
        "location": "Amritsar, India",
        "tagline": "golden sanctuary reflected in the Pool of Nectar",
    },
    "petronas_towers": {
        "display_name": "Petronas Twin Towers",
        "location": "Kuala Lumpur, Malaysia",
        "tagline": "twin steel pinnacles piercing the tropical sky",
    },
    "halong_bay": {
        "display_name": "Ha Long Bay",
        "location": "Quang Ninh, Vietnam",
        "tagline": "emerald waters weaving through limestone pillars",
    },
    "sigiriya": {
        "display_name": "Sigiriya Rock Fortress",
        "location": "Central Province, Sri Lanka",
        "tagline": "ancient palace atop a volcanic plug",
    },
    "potala_palace": {
        "display_name": "Potala Palace",
        "location": "Lhasa, Tibet",
        "tagline": "white and crimson fortress touching the sky",
    },
    "meiji_shrine": {
        "display_name": "Meiji Shrine",
        "location": "Tokyo, Japan",
        "tagline": "forested sanctuary in the heart of the city",
    },
    "gyeongbokgung": {
        "display_name": "Gyeongbokgung Palace",
        "location": "Seoul, South Korea",
        "tagline": "palace of shining happiness beneath the mountains",
    },
    "zhangjiajie": {
        "display_name": "Zhangjiajie",
        "location": "Hunan, China",
        "tagline": "sandstone pillars floating above the clouds",
    },
    "acropolis_athens": {
        "display_name": "Acropolis of Athens",
        "location": "Athens, Greece",
        "tagline": "marble citadel where democracy was born",
    },
    "blue_mosque": {
        "display_name": "Blue Mosque",
        "location": "Istanbul, Turkey",
        "tagline": "six minarets framing twenty thousand blue tiles",
    },
    "duomo_florence": {
        "display_name": "Florence Cathedral",
        "location": "Florence, Italy",
        "tagline": "Brunelleschi's dome crowning the Renaissance",
    },
    "tower_of_london": {
        "display_name": "Tower of London",
        "location": "London, England",
        "tagline": "fortress of kings, prisoners, and crown jewels",
    },
    "dubrovnik_walls": {
        "display_name": "Dubrovnik Old Town",
        "location": "Dubrovnik, Croatia",
        "tagline": "pearl of the Adriatic ringed in ancient stone",
    },
    "rothenburg": {
        "display_name": "Rothenburg ob der Tauber",
        "location": "Bavaria, Germany",
        "tagline": "half-timbered gem frozen in the Middle Ages",
    },
    "seville_alcazar": {
        "display_name": "Royal Alcazar of Seville",
        "location": "Seville, Spain",
        "tagline": "Moorish arches and gardens of paradise",
    },
    "matterhorn": {
        "display_name": "Matterhorn",
        "location": "Zermatt, Switzerland",
        "tagline": "pyramid peak mirrored in an Alpine lake",
    },
    "amalfi_coast": {
        "display_name": "Amalfi Coast",
        "location": "Campania, Italy",
        "tagline": "pastel villages cascading down sea cliffs",
    },
    "trolltunga": {
        "display_name": "Trolltunga",
        "location": "Hordaland, Norway",
        "tagline": "troll's tongue jutting over a glacial lake",
    },
    "meteora": {
        "display_name": "Meteora Monasteries",
        "location": "Thessaly, Greece",
        "tagline": "monasteries balanced on pillars of stone",
    },
    "niagara_falls": {
        "display_name": "Niagara Falls",
        "location": "Ontario/New York",
        "tagline": "thundering curtain between two nations",
    },
    "iguazu_falls": {
        "display_name": "Iguazu Falls",
        "location": "Argentina/Brazil",
        "tagline": "devil's throat roaring through the rainforest",
    },
    "easter_island": {
        "display_name": "Easter Island Moai",
        "location": "Easter Island, Chile",
        "tagline": "stone guardians watching the Pacific",
    },
    "tikal": {
        "display_name": "Tikal",
        "location": "Peten, Guatemala",
        "tagline": "Maya temples piercing the jungle canopy",
    },
    "antelope_canyon": {
        "display_name": "Antelope Canyon",
        "location": "Arizona, USA",
        "tagline": "light beams dancing through sculpted sandstone",
    },
    "monument_valley": {
        "display_name": "Monument Valley",
        "location": "Utah/Arizona, USA",
        "tagline": "towering buttes on the Navajo frontier",
    },
    "yellowstone": {
        "display_name": "Yellowstone",
        "location": "Wyoming, USA",
        "tagline": "prismatic springs above a sleeping supervolcano",
    },
    "sugarloaf_rio": {
        "display_name": "Sugarloaf Mountain",
        "location": "Rio de Janeiro, Brazil",
        "tagline": "granite dome rising from Guanabara Bay",
    },
    "lake_louise": {
        "display_name": "Lake Louise",
        "location": "Alberta, Canada",
        "tagline": "turquoise gem cradled by glacial peaks",
    },
    "uluru": {
        "display_name": "Uluru",
        "location": "Northern Territory, Australia",
        "tagline": "sacred monolith glowing red at sunset",
    },
    "tongariro": {
        "display_name": "Tongariro Alpine Crossing",
        "location": "North Island, New Zealand",
        "tagline": "volcanic landscape of emerald lakes and steam",
    },
    "great_barrier_reef": {
        "display_name": "Great Barrier Reef",
        "location": "Queensland, Australia",
        "tagline": "living mosaic visible from space",
    },
    "bora_bora": {
        "display_name": "Bora Bora",
        "location": "French Polynesia",
        "tagline": "turquoise lagoon ringed by a coral reef",
    },
    "burj_khalifa": {
        "display_name": "Burj Khalifa",
        "location": "Dubai, UAE",
        "tagline": "silver needle reaching for the desert stars",
    },
    "wadi_rum": {
        "display_name": "Wadi Rum",
        "location": "Aqaba, Jordan",
        "tagline": "valley of the moon carved in red sandstone",
    },
    "sheikh_zayed_mosque": {
        "display_name": "Sheikh Zayed Grand Mosque",
        "location": "Abu Dhabi, UAE",
        "tagline": "white marble cathedral of eighty-two domes",
    },
    "cappadocia": {
        "display_name": "Cappadocia",
        "location": "Nevsehir, Turkey",
        "tagline": "balloons drifting above fairy chimneys at dawn",
    },
    "northern_lights_iceland": {
        "display_name": "Northern Lights",
        "location": "Iceland",
        "tagline": "celestial curtains rippling across the Arctic sky",
    },
    "li_river_guilin": {
        "display_name": "Li River",
        "location": "Guilin, China",
        "tagline": "karst peaks floating on a jade ribbon",
    },
    "mysore_palace": {
        "display_name": "Mysore Palace",
        "location": "Mysore, India",
        "tagline": "Indo-Saracenic jewel blazing with light",
    },
    "banaue_rice_terraces": {
        "display_name": "Banaue Rice Terraces",
        "location": "Ifugao, Philippines",
        "tagline": "stairway to the sky carved by ancient hands",
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
