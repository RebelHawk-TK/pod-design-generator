"""Centralized landmark metadata and caption builders for all MDC video uploads.

Used by upload_tiktok.py, upload_instagram_api.py, and upload_youtube.py.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# All 97 landmarks — single source of truth
# ---------------------------------------------------------------------------

LANDMARKS = {
    "acropolis_athens": {"name": "Acropolis of Athens", "location": "Athens, Greece", "tags": ["acropolis", "athens", "ancientgreece"]},
    "amalfi_coast": {"name": "Amalfi Coast", "location": "Italy", "tags": ["amalficoast", "italy", "travel"]},
    "amsterdam_canals": {"name": "Amsterdam Canals", "location": "Amsterdam, Netherlands", "tags": ["amsterdam", "canals", "netherlands"]},
    "angkor_wat": {"name": "Angkor Wat", "location": "Cambodia", "tags": ["angkorwat", "cambodia", "ancienttemple"]},
    "antelope_canyon": {"name": "Antelope Canyon", "location": "Arizona, USA", "tags": ["antelopecanyon", "arizona", "slotcanyon"]},
    "bagan_temples": {"name": "Bagan Temples", "location": "Myanmar", "tags": ["bagan", "myanmar", "temples"]},
    "banaue_rice_terraces": {"name": "Banaue Rice Terraces", "location": "Philippines", "tags": ["banaue", "philippines", "terraces"]},
    "big_ben": {"name": "Big Ben", "location": "London, England", "tags": ["bigben", "london", "unitedkingdom"]},
    "blue_mosque": {"name": "Blue Mosque", "location": "Istanbul, Turkey", "tags": ["bluemosque", "istanbul", "ottoman"]},
    "bora_bora": {"name": "Bora Bora", "location": "French Polynesia", "tags": ["borabora", "frenchpolynesia", "paradise"]},
    "borobudur": {"name": "Borobudur", "location": "Java, Indonesia", "tags": ["borobudur", "indonesia", "buddhisttemple"]},
    "bruges_medieval": {"name": "Bruges", "location": "Belgium", "tags": ["bruges", "belgium", "medieval"]},
    "burj_khalifa": {"name": "Burj Khalifa", "location": "Dubai, UAE", "tags": ["burjkhalifa", "dubai", "tallestbuilding"]},
    "cappadocia": {"name": "Cappadocia", "location": "Turkey", "tags": ["cappadocia", "turkey", "hotairballoon"]},
    "charles_bridge": {"name": "Charles Bridge", "location": "Prague, Czech Republic", "tags": ["charlesbridge", "prague", "czechia"]},
    "chefchaouen": {"name": "Chefchaouen", "location": "Morocco", "tags": ["chefchaouen", "morocco", "bluecity"]},
    "chichen_itza": {"name": "Chichen Itza", "location": "Mexico", "tags": ["chichenitza", "mexico", "mayanruins"]},
    "christ_redeemer": {"name": "Christ the Redeemer", "location": "Rio de Janeiro, Brazil", "tags": ["christtheredeemer", "riodejaneiro", "brazil"]},
    "colosseum": {"name": "Colosseum", "location": "Rome, Italy", "tags": ["colosseum", "rome", "italyart"]},
    "djemaa_el_fna": {"name": "Djemaa el-Fna", "location": "Marrakech, Morocco", "tags": ["djemaa", "marrakech", "morocco"]},
    "dubrovnik_walls": {"name": "Dubrovnik Walls", "location": "Dubrovnik, Croatia", "tags": ["dubrovnik", "croatia", "medieval"]},
    "duomo_florence": {"name": "Florence Cathedral", "location": "Florence, Italy", "tags": ["duomo", "florence", "italy"]},
    "easter_island": {"name": "Easter Island", "location": "Chile", "tags": ["easterisland", "moai", "chile"]},
    "edinburgh_old_town": {"name": "Edinburgh Old Town", "location": "Scotland", "tags": ["edinburgh", "scotland", "oldtown"]},
    "eiffel_tower": {"name": "Eiffel Tower", "location": "Paris, France", "tags": ["eiffeltower", "paris", "parisart"]},
    "fushimi_inari": {"name": "Fushimi Inari Shrine", "location": "Kyoto, Japan", "tags": ["fushimiinari", "kyoto", "japan"]},
    "giants_causeway": {"name": "Giant's Causeway", "location": "Northern Ireland", "tags": ["giantscauseway", "ireland", "naturalwonder"]},
    "golden_gate": {"name": "Golden Gate Bridge", "location": "San Francisco, USA", "tags": ["goldengatebridge", "sanfrancisco", "california"]},
    "golden_temple_amritsar": {"name": "Golden Temple", "location": "Amritsar, India", "tags": ["goldentemple", "amritsar", "india"]},
    "great_barrier_reef": {"name": "Great Barrier Reef", "location": "Australia", "tags": ["greatbarrierreef", "australia", "coralreef"]},
    "great_wall": {"name": "Great Wall", "location": "China", "tags": ["greatwallofchina", "china", "wonderoftheworld"]},
    "guanajuato": {"name": "Guanajuato", "location": "Mexico", "tags": ["guanajuato", "mexico", "colorfulcity"]},
    "gyeongbokgung": {"name": "Gyeongbokgung Palace", "location": "Seoul, South Korea", "tags": ["gyeongbokgung", "seoul", "korea"]},
    "hagia_sophia": {"name": "Hagia Sophia", "location": "Istanbul, Turkey", "tags": ["hagiasophia", "istanbul", "turkeytravel"]},
    "hallgrimskirkja": {"name": "Hallgrimskirkja", "location": "Reykjavik, Iceland", "tags": ["hallgrimskirkja", "reykjavik", "iceland"]},
    "halong_bay": {"name": "Halong Bay", "location": "Vietnam", "tags": ["halongbay", "vietnam", "limestone"]},
    "hapenny_bridge": {"name": "Ha'penny Bridge", "location": "Dublin, Ireland", "tags": ["hapenny", "dublin", "ireland"]},
    "havana_vieja": {"name": "Havana Vieja", "location": "Havana, Cuba", "tags": ["havana", "cuba", "oldtown"]},
    "hawa_mahal": {"name": "Hawa Mahal", "location": "Jaipur, India", "tags": ["hawamahal", "jaipur", "india"]},
    "hoi_an": {"name": "Hoi An Ancient Town", "location": "Vietnam", "tags": ["hoian", "vietnam", "lanterns"]},
    "iguazu_falls": {"name": "Iguazu Falls", "location": "Argentina/Brazil", "tags": ["iguazufalls", "waterfall", "southamerica"]},
    "lake_louise": {"name": "Lake Louise", "location": "Alberta, Canada", "tags": ["lakelouise", "canada", "rockymountains"]},
    "lalibela_churches": {"name": "Lalibela Churches", "location": "Ethiopia", "tags": ["lalibela", "ethiopia", "churches"]},
    "li_river_guilin": {"name": "Li River", "location": "Guilin, China", "tags": ["liriver", "guilin", "china"]},
    "machu_picchu": {"name": "Machu Picchu", "location": "Peru", "tags": ["machupicchu", "peru", "incatrail"]},
    "matterhorn": {"name": "Matterhorn", "location": "Switzerland", "tags": ["matterhorn", "switzerland", "alps"]},
    "meiji_shrine": {"name": "Meiji Shrine", "location": "Tokyo, Japan", "tags": ["meijishrine", "tokyo", "japan"]},
    "meteora": {"name": "Meteora", "location": "Greece", "tags": ["meteora", "greece", "monasteries"]},
    "milford_sound": {"name": "Milford Sound", "location": "New Zealand", "tags": ["milfordsound", "newzealand", "fjord"]},
    "moai": {"name": "Moai Statues", "location": "Easter Island", "tags": ["moai", "easterisland", "rapanui"]},
    "mont_saint_michel": {"name": "Mont Saint-Michel", "location": "Normandy, France", "tags": ["montsaintmichel", "france", "medieval"]},
    "monument_valley": {"name": "Monument Valley", "location": "Arizona/Utah, USA", "tags": ["monumentvalley", "arizona", "desert"]},
    "moraine_lake": {"name": "Moraine Lake", "location": "Alberta, Canada", "tags": ["morainelake", "canada", "mountains"]},
    "mount_fuji": {"name": "Mount Fuji", "location": "Japan", "tags": ["mountfuji", "japan", "fujisan"]},
    "mysore_palace": {"name": "Mysore Palace", "location": "Mysore, India", "tags": ["mysorepalace", "mysore", "india"]},
    "neuschwanstein": {"name": "Neuschwanstein", "location": "Bavaria, Germany", "tags": ["neuschwanstein", "bavaria", "fairytalecastle"]},
    "niagara_falls": {"name": "Niagara Falls", "location": "USA/Canada", "tags": ["niagarafalls", "waterfall", "naturalwonder"]},
    "northern_lights_iceland": {"name": "Northern Lights", "location": "Iceland", "tags": ["northernlights", "iceland", "aurora"]},
    "notre_dame": {"name": "Notre-Dame", "location": "Paris, France", "tags": ["notredame", "paris", "gothicart"]},
    "nyhavn": {"name": "Nyhavn", "location": "Copenhagen, Denmark", "tags": ["nyhavn", "copenhagen", "denmark"]},
    "parthenon": {"name": "Parthenon", "location": "Athens, Greece", "tags": ["parthenon", "athens", "greekhistory"]},
    "petra": {"name": "Petra", "location": "Jordan", "tags": ["petra", "jordan", "rosecity"]},
    "petronas_towers": {"name": "Petronas Towers", "location": "Kuala Lumpur, Malaysia", "tags": ["petronastowers", "malaysia", "skyline"]},
    "plitvice_lakes": {"name": "Plitvice Lakes", "location": "Croatia", "tags": ["plitvicelakes", "croatia", "waterfalls"]},
    "ponte_vecchio": {"name": "Ponte Vecchio", "location": "Florence, Italy", "tags": ["pontevecchio", "florence", "italy"]},
    "potala_palace": {"name": "Potala Palace", "location": "Lhasa, Tibet", "tags": ["potalapalace", "lhasa", "tibet"]},
    "pyramids_giza": {"name": "Pyramids of Giza", "location": "Egypt", "tags": ["pyramidsofgiza", "egypt", "ancientegypt"]},
    "rialto_bridge": {"name": "Rialto Bridge", "location": "Venice, Italy", "tags": ["rialto", "venice", "italy"]},
    "rijksmuseum": {"name": "Rijksmuseum", "location": "Amsterdam, Netherlands", "tags": ["rijksmuseum", "amsterdam", "museum"]},
    "rothenburg": {"name": "Rothenburg ob der Tauber", "location": "Germany", "tags": ["rothenburg", "germany", "medieval"]},
    "sagrada_familia": {"name": "Sagrada Familia", "location": "Barcelona, Spain", "tags": ["sagradafamilia", "barcelona", "gaudi"]},
    "santorini": {"name": "Santorini", "location": "Greece", "tags": ["santorini", "greece", "greekislands"]},
    "serengeti": {"name": "Serengeti", "location": "Tanzania", "tags": ["serengeti", "safari", "wildlife"]},
    "seville_alcazar": {"name": "Royal Alcazar of Seville", "location": "Seville, Spain", "tags": ["alcazar", "seville", "spain"]},
    "sheikh_zayed_mosque": {"name": "Sheikh Zayed Mosque", "location": "Abu Dhabi, UAE", "tags": ["sheikhzayed", "abudhabi", "mosque"]},
    "sigiriya": {"name": "Sigiriya", "location": "Sri Lanka", "tags": ["sigiriya", "srilanka", "rockfortress"]},
    "st_basils": {"name": "St. Basil's Cathedral", "location": "Moscow, Russia", "tags": ["stbasils", "moscow", "russianart"]},
    "statue_of_liberty": {"name": "Statue of Liberty", "location": "New York, USA", "tags": ["statueofliberty", "newyork", "nyc"]},
    "stonehenge": {"name": "Stonehenge", "location": "England", "tags": ["stonehenge", "england", "ancientmonument"]},
    "sugarloaf_rio": {"name": "Sugarloaf Mountain", "location": "Rio de Janeiro, Brazil", "tags": ["sugarloaf", "rio", "brazil"]},
    "sydney_opera": {"name": "Sydney Opera House", "location": "Sydney, Australia", "tags": ["sydneyoperahouse", "sydney", "australia"]},
    "table_mountain": {"name": "Table Mountain", "location": "Cape Town, South Africa", "tags": ["tablemountain", "capetown", "southafrica"]},
    "taj_mahal": {"name": "Taj Mahal", "location": "Agra, India", "tags": ["tajmahal", "india", "incredibleindia"]},
    "temple_bar": {"name": "Temple Bar", "location": "Dublin, Ireland", "tags": ["templebar", "dublin", "ireland"]},
    "terracotta_warriors": {"name": "Terracotta Warriors", "location": "Xi'an, China", "tags": ["terracottawarriors", "xian", "china"]},
    "tikal": {"name": "Tikal", "location": "Guatemala", "tags": ["tikal", "guatemala", "maya"]},
    "tongariro": {"name": "Tongariro National Park", "location": "New Zealand", "tags": ["tongariro", "newzealand", "nationalpark"]},
    "tower_of_london": {"name": "Tower of London", "location": "London, England", "tags": ["toweroflondon", "london", "castle"]},
    "tower_of_pisa": {"name": "Tower of Pisa", "location": "Pisa, Italy", "tags": ["towerofpisa", "pisa", "leaningtower"]},
    "trolltunga": {"name": "Trolltunga", "location": "Norway", "tags": ["trolltunga", "norway", "cliff"]},
    "twelve_apostles": {"name": "Twelve Apostles", "location": "Victoria, Australia", "tags": ["twelveapostles", "australia", "coastalformation"]},
    "uluru": {"name": "Uluru", "location": "Australia", "tags": ["uluru", "australia", "outback"]},
    "victoria_falls": {"name": "Victoria Falls", "location": "Zambia/Zimbabwe", "tags": ["victoriafalls", "africa", "waterfall"]},
    "wadi_rum": {"name": "Wadi Rum", "location": "Jordan", "tags": ["wadirum", "jordan", "desert"]},
    "yellowstone": {"name": "Yellowstone", "location": "Wyoming, USA", "tags": ["yellowstone", "nationalpark", "geysers"]},
    "zanzibar_stone_town": {"name": "Zanzibar Stone Town", "location": "Zanzibar, Tanzania", "tags": ["zanzibar", "tanzania", "stonetown"]},
    "zhangjiajie": {"name": "Zhangjiajie", "location": "Hunan, China", "tags": ["zhangjiajie", "china", "avatarmountains"]},
}


# ---------------------------------------------------------------------------
# Shared tag lists
# ---------------------------------------------------------------------------

TIKTOK_PROMO_TAGS = [
    "fineart", "artprint", "homedecor", "wallart", "moderndesignconcept",
    "styletransfer", "aiart", "travelart", "landmarks", "fyp",
]

TIKTOK_TRAVEL_TAGS = [
    "travelfacts", "history", "didyouknow", "worldwonders", "moderndesignconcept",
    "travel", "landmarks", "explore", "fyp",
]

TIKTOK_STOCK_TAGS = [
    "travel", "beautifulplaces", "worldwonders", "moderndesignconcept",
    "wanderlust", "explore", "landmarks", "fyp",
]

INSTAGRAM_PROMO_TAGS = [
    "fineart", "artprint", "homedecor", "wallart", "moderndesignconcept",
    "styletransfer", "aiart", "travelart", "landmarks", "artlovers",
    "posterart", "gallerywall", "interiordesign", "reels",
]

INSTAGRAM_TRAVEL_TAGS = [
    "travelfacts", "history", "didyouknow", "worldwonders", "moderndesignconcept",
    "travel", "landmarks", "explore", "travelreels", "wanderlust",
    "bucketlist", "travelgram", "reels",
]

INSTAGRAM_STOCK_TAGS = [
    "travel", "beautifulplaces", "worldwonders", "moderndesignconcept",
    "wanderlust", "explore", "landmarks", "travelgram", "reels",
    "travelphotography", "worldtravel",
]

YOUTUBE_PROMO_TAGS = [
    "fineart", "artprint", "homedecor", "wallart", "moderndesignconcept", "shorts",
]

YOUTUBE_TRAVEL_TAGS = [
    "travelfacts", "history", "didyouknow", "worldwonders", "moderndesignconcept", "shorts",
]

# YouTube category IDs
YOUTUBE_CATEGORY_ENTERTAINMENT = "24"
YOUTUBE_CATEGORY_TRAVEL = "19"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_landmark(landmark_id: str) -> dict:
    """Get landmark info, falling back to formatting the ID as a name."""
    info = LANDMARKS.get(landmark_id, {})
    if not info:
        return {
            "name": landmark_id.replace("_", " ").title(),
            "location": "",
            "tags": [],
        }
    return info


def extract_video_info(filename_stem: str) -> tuple[str, str]:
    """Extract landmark ID and video type from filename.

    Returns: (landmark_id, video_type) where video_type is 'promo', 'travel', or 'stock'.
    """
    for suffix in ("_travel_a", "_travel_b"):
        if filename_stem.endswith(suffix):
            return filename_stem[: -len(suffix)], "travel"
    for suffix in ("_stock_a", "_stock_b"):
        if filename_stem.endswith(suffix):
            return filename_stem[: -len(suffix)], "stock"
    return filename_stem, "promo"


# ---------------------------------------------------------------------------
# TikTok captions
# ---------------------------------------------------------------------------

def build_tiktok_caption(landmark_id: str, *, video_type: str = "promo") -> str:
    """Build a TikTok caption with hashtags."""
    info = get_landmark(landmark_id)
    name = info["name"]
    location = info["location"]
    specific_tags = info["tags"]

    if video_type == "travel":
        caption = f"Incredible facts about the {name}"
        if location:
            caption += f" | {location}"
        caption += "\nMore at moderndesignconcept.com"
        all_tags = specific_tags + TIKTOK_TRAVEL_TAGS
    elif video_type == "stock":
        caption = f"The beauty of {name}"
        if location:
            caption += f" | {location}"
        caption += "\nShop: moderndesignconcept.com"
        all_tags = specific_tags + TIKTOK_STOCK_TAGS
    else:
        caption = f"{name} reimagined as fine art"
        if location:
            caption += f" | {location}"
        caption += "\nShop: moderndesignconcept.com"
        all_tags = specific_tags + TIKTOK_PROMO_TAGS

    hashtags = " ".join(f"#{t}" for t in all_tags[:15])
    caption += f"\n{hashtags}"
    return caption[:2200]


# ---------------------------------------------------------------------------
# Instagram captions
# ---------------------------------------------------------------------------

def build_instagram_caption(landmark_id: str, *, video_type: str = "promo") -> str:
    """Build an Instagram caption with hashtags."""
    info = get_landmark(landmark_id)
    name = info["name"]
    location = info["location"]
    specific_tags = info["tags"]

    if video_type == "travel":
        caption = f"Incredible facts about the {name}"
        if location:
            caption += f"\n📍 {location}"
        caption += "\n\nMore art inspired by world landmarks → moderndesignconcept.com (link in bio)"
        all_tags = specific_tags + INSTAGRAM_TRAVEL_TAGS
    elif video_type == "stock":
        caption = f"The beauty of {name}"
        if location:
            caption += f"\n📍 {location}"
        caption += "\n\nShop art prints inspired by world landmarks → moderndesignconcept.com (link in bio)"
        all_tags = specific_tags + INSTAGRAM_STOCK_TAGS
    else:
        caption = f"{name} reimagined as fine art 🎨"
        if location:
            caption += f"\n📍 {location}"
        caption += "\n\nShop the full collection → moderndesignconcept.com (link in bio)"
        all_tags = specific_tags + INSTAGRAM_PROMO_TAGS

    hashtags = " ".join(f"#{t}" for t in all_tags[:20])
    caption += f"\n\n{hashtags}"
    return caption[:2200]


# ---------------------------------------------------------------------------
# YouTube metadata
# ---------------------------------------------------------------------------

def build_youtube_metadata(landmark_id: str, *, video_type: str = "promo") -> dict:
    """Build YouTube title, description, tags, and category."""
    info = get_landmark(landmark_id)
    name = info["name"]
    location = info["location"]
    specific_tags = info["tags"]

    is_travel = video_type in ("travel", "stock")

    if is_travel:
        title = f"Incredible facts about {name}"
        if location:
            title += f" | {location}"
        description = (
            f"Incredible facts about the {name}"
            f"{f' in {location}' if location else ''}.\n\n"
            f"More art and travel content at moderndesignconcept.com\n\n"
            f"#Shorts #travel #history #landmarks #didyouknow"
        )
        tags = specific_tags + YOUTUBE_TRAVEL_TAGS
        category = YOUTUBE_CATEGORY_TRAVEL
    else:
        title = f"{name} reimagined as fine art"
        if location:
            title += f" | {location}"
        description = (
            f"{name} reimagined through classic art styles using neural style transfer.\n\n"
            f"Shop prints, posters & tees: https://moderndesignconcept.com\n\n"
            f"#Shorts #fineart #artprint #wallart #homedecor"
        )
        tags = specific_tags + YOUTUBE_PROMO_TAGS
        category = YOUTUBE_CATEGORY_ENTERTAINMENT

    return {
        "title": title[:100],
        "description": description,
        "tags": tags[:15],
        "category": category,
    }
