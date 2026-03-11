#!/usr/bin/env python3
"""Download stock video clips from Pexels for landmark travel videos.

Downloads 4 short portrait clips per landmark (100 clips total) for use as
stock-footage alternatives to Ken Burns art-style travel videos.

Setup:
    Create .pexels_config.json with {"api_key": "YOUR_KEY"}

Usage:
    python3 download_stock_clips.py --landmark eiffel_tower    # One landmark
    python3 download_stock_clips.py --all                       # All 25
    python3 download_stock_clips.py --list                      # Show landmarks
    python3 download_stock_clips.py --all --force               # Re-download all
    python3 download_stock_clips.py --all --dry-run             # Preview only
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import requests

PROJECT_DIR = Path(__file__).parent

from keychain_config import load_config as _load_keychain_config
CLIPS_DIR = PROJECT_DIR / "output" / "stock_clips"

CLIPS_PER_LANDMARK = 4
API_BASE = "https://api.pexels.com/videos/search"

# Optimized search queries per landmark — specific enough for relevant results
SEARCH_QUERIES: dict[str, str] = {
    "eiffel_tower": "Eiffel Tower Paris",
    "taj_mahal": "Taj Mahal India",
    "colosseum": "Colosseum Rome",
    "great_wall": "Great Wall China",
    "notre_dame": "Notre Dame Paris cathedral",
    "neuschwanstein": "Neuschwanstein Castle Bavaria",
    "mount_fuji": "Mount Fuji Japan",
    "golden_gate": "Golden Gate Bridge San Francisco",
    "sydney_opera": "Sydney Opera House",
    "santorini": "Santorini Greece",
    "angkor_wat": "Angkor Wat Cambodia temple",
    "machu_picchu": "Machu Picchu Peru",
    "sagrada_familia": "Sagrada Familia Barcelona",
    "parthenon": "Parthenon Athens Greece",
    "stonehenge": "Stonehenge England",
    "moai": "Easter Island Moai statues",
    "pyramids_giza": "Pyramids Giza Egypt",
    "petra": "Petra Jordan ancient city",
    "st_basils": "Saint Basil Cathedral Moscow",
    "chichen_itza": "Chichen Itza Mexico pyramid",
    "christ_redeemer": "Christ Redeemer Rio de Janeiro",
    "hagia_sophia": "Hagia Sophia Istanbul",
    "tower_of_pisa": "Leaning Tower Pisa Italy",
    "big_ben": "Big Ben London",
    "statue_of_liberty": "Statue of Liberty New York",
    # Phase 2 landmarks
    "amsterdam_canals": "Amsterdam canals Netherlands",
    "bagan_temples": "Bagan temples Myanmar",
    "bruges_medieval": "Bruges Belgium medieval",
    "charles_bridge": "Charles Bridge Prague",
    "chefchaouen": "Chefchaouen Morocco blue city",
    "edinburgh_old_town": "Edinburgh Old Town Scotland",
    "fushimi_inari": "Fushimi Inari shrine Kyoto torii",
    "giants_causeway": "Giant's Causeway Northern Ireland",
    "guanajuato": "Guanajuato Mexico colorful",
    "hallgrimskirkja": "Hallgrimskirkja Reykjavik Iceland",
    "hapenny_bridge": "Ha'penny Bridge Dublin Ireland",
    "havana_vieja": "Old Havana Cuba",
    "hawa_mahal": "Hawa Mahal Jaipur India",
    "hoi_an": "Hoi An Vietnam lanterns",
    "milford_sound": "Milford Sound New Zealand fjord",
    "mont_saint_michel": "Mont Saint Michel France",
    "moraine_lake": "Moraine Lake Banff Canada",
    "nyhavn": "Nyhavn Copenhagen Denmark",
    "plitvice_lakes": "Plitvice Lakes Croatia waterfalls",
    "ponte_vecchio": "Ponte Vecchio Florence Italy",
    "rialto_bridge": "Rialto Bridge Venice Italy",
    "rijksmuseum": "Rijksmuseum Amsterdam Netherlands",
    "temple_bar": "Temple Bar Dublin Ireland",
    "twelve_apostles": "Twelve Apostles Great Ocean Road Australia",
    "zanzibar_stone_town": "Zanzibar Stone Town Tanzania",
    # Phase 3 landmarks
    "acropolis_athens": "Acropolis Athens Greece",
    "amalfi_coast": "Amalfi Coast Italy",
    "antelope_canyon": "Antelope Canyon Arizona",
    "banaue_rice_terraces": "Banaue Rice Terraces Philippines",
    "blue_mosque": "Blue Mosque Istanbul Turkey",
    "bora_bora": "Bora Bora French Polynesia",
    "borobudur": "Borobudur Temple Java Indonesia",
    "burj_khalifa": "Burj Khalifa Dubai",
    "cappadocia": "Cappadocia Turkey balloon",
    "djemaa_el_fna": "Djemaa el Fna Marrakech Morocco",
    "dubrovnik_walls": "Dubrovnik Old Town walls Croatia",
    "duomo_florence": "Florence Cathedral Duomo Italy",
    "easter_island": "Easter Island Chile Moai",
    "golden_temple_amritsar": "Golden Temple Amritsar India",
    "great_barrier_reef": "Great Barrier Reef Australia",
    "gyeongbokgung": "Gyeongbokgung Palace Seoul Korea",
    "halong_bay": "Ha Long Bay Vietnam",
    "iguazu_falls": "Iguazu Falls Argentina Brazil",
    "lake_louise": "Lake Louise Banff Canada",
    "lalibela_churches": "Lalibela rock churches Ethiopia",
    "li_river_guilin": "Li River Guilin China karst",
    "matterhorn": "Matterhorn Alps Switzerland",
    "meiji_shrine": "Meiji Shrine Tokyo Japan",
    "meteora": "Meteora monasteries Greece",
    "monument_valley": "Monument Valley Utah Arizona",
    "mysore_palace": "Mysore Palace India",
    "niagara_falls": "Niagara Falls waterfall",
    "northern_lights_iceland": "Northern Lights Iceland aurora",
    "petronas_towers": "Petronas Towers Kuala Lumpur Malaysia",
    "potala_palace": "Potala Palace Lhasa Tibet",
    "rothenburg": "Rothenburg ob der Tauber Germany",
    "serengeti": "Serengeti National Park Tanzania",
    "seville_alcazar": "Alcazar Seville Spain",
    "sheikh_zayed_mosque": "Sheikh Zayed Mosque Abu Dhabi",
    "sigiriya": "Sigiriya Lion Rock Sri Lanka",
    "sugarloaf_rio": "Sugarloaf Mountain Rio de Janeiro",
    "table_mountain": "Table Mountain Cape Town South Africa",
    "terracotta_warriors": "Terracotta Warriors Xian China",
    "tikal": "Tikal Temple Guatemala Maya",
    "tongariro": "Tongariro Alpine Crossing New Zealand",
    "tower_of_london": "Tower of London England",
    "trolltunga": "Trolltunga Norway cliff",
    "uluru": "Uluru Ayers Rock Australia",
    "victoria_falls": "Victoria Falls Zambia Zimbabwe",
    "wadi_rum": "Wadi Rum Jordan desert",
    "yellowstone": "Yellowstone National Park geyser",
    "zhangjiajie": "Zhangjiajie National Forest China",
}


def load_config() -> dict:
    return _load_keychain_config("pexels")


def pexels_search(api_key: str, query: str) -> list[dict]:
    """Search Pexels for portrait videos matching query."""
    params = {
        "query": query,
        "orientation": "portrait",
        "size": "large",
        "per_page": 15,
    }
    headers = {"Authorization": api_key}

    resp = requests.get(API_BASE, params=params, headers=headers, timeout=30)

    if resp.status_code == 429:
        print(f"  Rate limited — waiting 60s...")
        time.sleep(60)
        resp = requests.get(API_BASE, params=params, headers=headers, timeout=30)

    resp.raise_for_status()
    return resp.json().get("videos", [])


def pick_best_file(video: dict) -> dict | None:
    """Pick the best portrait video file from Pexels video_files array.

    Prefers HD portrait (1080x1920) or closest match.
    """
    files = video.get("video_files", [])
    if not files:
        return None

    # Filter for reasonable quality files with video type
    candidates = [
        f for f in files
        if f.get("file_type", "").startswith("video/")
        and f.get("width", 0) > 0
        and f.get("height", 0) > 0
    ]
    if not candidates:
        return files[0] if files else None

    # Prefer portrait files (height > width)
    portrait = [f for f in candidates if f["height"] > f["width"]]
    pool = portrait if portrait else candidates

    # Sort by height descending, prefer closest to 1920
    pool.sort(key=lambda f: abs(f["height"] - 1920))
    return pool[0]


def download_file(url: str, dest: Path, retries: int = 3) -> bool:
    """Download a file with retry logic."""
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=120, stream=True)
            resp.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except (requests.RequestException, TimeoutError) as e:
            if attempt < retries - 1:
                wait = 5 * (attempt + 1)
                print(f"    Retry {attempt + 1}/{retries} in {wait}s: {e}")
                time.sleep(wait)
            else:
                print(f"    Failed after {retries} attempts: {e}")
                return False
    return False


def download_landmark(api_key: str, landmark_id: str, *, force: bool = False, dry_run: bool = False) -> int:
    """Download stock clips for one landmark. Returns count downloaded."""
    query = SEARCH_QUERIES.get(landmark_id)
    if not query:
        print(f"  No search query for '{landmark_id}'")
        return 0

    clip_dir = CLIPS_DIR / landmark_id
    clip_dir.mkdir(parents=True, exist_ok=True)

    # Check existing clips
    existing = [f for f in clip_dir.glob("clip_*.mp4") if f.stat().st_size > 0]
    if len(existing) >= CLIPS_PER_LANDMARK and not force:
        print(f"  {landmark_id}: {len(existing)} clips exist (skip). Use --force to re-download.")
        return 0

    print(f"  Searching: \"{query}\"...")
    if dry_run:
        print(f"  DRY RUN — would download {CLIPS_PER_LANDMARK} clips to {clip_dir}")
        return CLIPS_PER_LANDMARK

    videos = pexels_search(api_key, query)
    if not videos:
        print(f"  No results for '{query}'")
        return 0

    # Filter videos by duration (5-30s ideal for clips)
    suitable = [
        v for v in videos
        if 5 <= v.get("duration", 0) <= 60
    ]
    if not suitable:
        suitable = videos  # Fallback to unfiltered

    downloaded = 0
    for i in range(min(CLIPS_PER_LANDMARK, len(suitable))):
        clip_path = clip_dir / f"clip_{i + 1}.mp4"

        if clip_path.exists() and clip_path.stat().st_size > 0 and not force:
            print(f"    clip_{i + 1}.mp4 exists (skip)")
            downloaded += 1
            continue

        video = suitable[i]
        best_file = pick_best_file(video)
        if not best_file:
            print(f"    clip_{i + 1}: no suitable file found")
            continue

        file_url = best_file.get("link", "")
        res = f"{best_file.get('width', '?')}x{best_file.get('height', '?')}"
        dur = video.get("duration", "?")
        size_mb = (best_file.get("size", 0) or 0) / (1024 * 1024)

        print(f"    clip_{i + 1}.mp4: {res}, {dur}s, {size_mb:.1f}MB ...")
        if download_file(file_url, clip_path):
            actual_mb = clip_path.stat().st_size / (1024 * 1024)
            print(f"    -> Downloaded ({actual_mb:.1f}MB)")
            downloaded += 1
        else:
            print(f"    -> Download failed")

    return downloaded


def list_landmarks() -> None:
    """Show landmarks with their search queries and existing clip counts."""
    print(f"\n{'ID':<25} {'Query':<40} {'Clips'}")
    print("-" * 75)
    total_clips = 0
    for lid in sorted(SEARCH_QUERIES.keys()):
        query = SEARCH_QUERIES[lid]
        clip_dir = CLIPS_DIR / lid
        existing = len(list(clip_dir.glob("clip_*.mp4"))) if clip_dir.exists() else 0
        total_clips += existing
        status = f"{existing}/{CLIPS_PER_LANDMARK}"
        print(f"{lid:<25} {query:<40} {status}")
    print(f"\nTotal: {len(SEARCH_QUERIES)} landmarks, {total_clips}/{len(SEARCH_QUERIES) * CLIPS_PER_LANDMARK} clips")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download stock video clips from Pexels for landmark travel videos.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--landmark", type=str, help="Download clips for one landmark")
    group.add_argument("--all", action="store_true", help="Download clips for all 25 landmarks")
    group.add_argument("--list", action="store_true", help="List landmarks and clip status")

    parser.add_argument("--force", action="store_true", help="Re-download existing clips")
    parser.add_argument("--dry-run", action="store_true", help="Preview without downloading")

    args = parser.parse_args()

    if args.list:
        list_landmarks()
        return

    config = load_config()
    api_key = config["api_key"]

    if args.landmark:
        if args.landmark not in SEARCH_QUERIES:
            print(f"Error: Unknown landmark '{args.landmark}'")
            print("Use --list to see available landmarks.")
            sys.exit(1)
        landmark_ids = [args.landmark]
    else:
        landmark_ids = sorted(SEARCH_QUERIES.keys())

    print(f"\nPexels Stock Clip Downloader")
    print(f"============================")
    print(f"Landmarks:  {len(landmark_ids)}")
    print(f"Clips each: {CLIPS_PER_LANDMARK}")
    print(f"Output:     {CLIPS_DIR}")
    print(f"Force:      {args.force}")
    print()

    total_downloaded = 0
    for i, lid in enumerate(landmark_ids, 1):
        print(f"[{i}/{len(landmark_ids)}] {lid}")
        count = download_landmark(api_key, lid, force=args.force, dry_run=args.dry_run)
        total_downloaded += count
        # Small delay between API searches to be polite
        if i < len(landmark_ids) and not args.dry_run:
            time.sleep(1)

    print(f"\nComplete: {total_downloaded} clips downloaded")


if __name__ == "__main__":
    main()
