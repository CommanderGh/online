#!/usr/bin/env python3
"""
main.py
Orchestrate scraping, cleaning and saving of headlines from the Guardian.
"""


"""
scraper.py
Responsible for network I/O and basic HTML parsing.
"""

import requests
from bs4 import BeautifulSoup
from typing import List

class FetchError(RuntimeError):
    """Raised when the network or HTML layer fails."""

def fetch_headlines(url: str) -> List[str]:
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise FetchError(f"Network failure: {exc}") from exc

    try:
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as exc:
        raise FetchError(f"BeautifulSoup failure: {exc}") from exc

    # The Guardian uses <h3> tags for most headlines
    h3_tags = soup.find_all("h3")
    if not h3_tags:
        raise FetchError("No <h3> tags found – HTML structure may have changed.")

    headlines = [h.get_text(strip=True) for h in h3_tags if h.get_text(strip=True)]
    if not headlines:
        raise FetchError("No text extracted from <h3> tags.")
    return headlines

from scraper import fetch_headlines
from text_utils import clean_headlines, save_headlines
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

def main():
    try:
        raw = fetch_headlines("https://www.theguardian.com/international")
        cleaned = clean_headlines(raw)
        save_headlines(cleaned, "headlines.txt")
        logging.info("✅ Job finished – %d headlines saved.", len(cleaned))
    except Exception as exc:
        logging.error("❌ Fatal error: %s", exc)
        sys.exit(1)

if __name__ == "__main__":
    main()

    """
text_utils.py
Clean, deduplicate and persist headlines.
"""

import string
from typing import List

STOP_WORDS = {"live", "video", "podcast", "sport"}   # simple filter example

def clean_headlines(raw: List[str]) -> List[str]:
    cleaned = []
    seen = set()
    for line in raw:
        # basic string cleaning
        line = line.strip()
        line = line.translate(str.maketrans("", "", string.punctuation))
        line = line.title()
        if line and line not in seen:
            if not any(sw in line.lower() for sw in STOP_WORDS):
                cleaned.append(line)
                seen.add(line)
    return cleaned

def save_headlines(headlines: List[str], path: str) -> None:
    try:
        with open(path, "w", encoding="utf-8") as fh:
            for h in headlines:
                fh.write(h + "\n")
    except OSError as exc:
        raise RuntimeError(f"Cannot save file: {exc}") from exc