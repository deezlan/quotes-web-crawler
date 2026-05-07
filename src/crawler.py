"""
Crawls all pages of the target website, respecting a politeness
window of at least 6 seconds between requests.
"""

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"
POLITENESS_WINDOW = 6  # seconds between requests


def get_page(url: str) -> BeautifulSoup | None:
    """
    Fetch a single page and return a BeautifulSoup object.
    Returns None if the request fails.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"[crawler] Failed to fetch {url}: {e}")
        return None