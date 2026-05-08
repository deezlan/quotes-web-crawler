"""
crawler.py - Web crawler for quotes.toscrape.com

Crawls all pages of the target website, respecting a politeness
window of at least 6 seconds between requests.
"""

import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

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


def get_links(soup: BeautifulSoup, current_url: str) -> list[str]:
    """
    Extract all internal links from a page.
    Returns absolute URLs belonging to the same domain.
    """
    links = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        absolute = urljoin(current_url, href)
        # Only keep links within the same domain
        if urlparse(absolute).netloc == urlparse(BASE_URL).netloc:
            links.append(absolute)
    return links


def get_text(soup: BeautifulSoup) -> str:
    """
    Extract visible text content from a page.
    Strips scripts, styles, and other non-visible elements.
    """
    for tag in soup(["script", "style", "meta", "head"]):
        tag.decompose()
    return soup.get_text(separator=" ")


def crawl() -> dict[str, str]:
    """
    Crawl the entire website starting from BASE_URL.
    Returns a dict mapping page URL -> raw page text.
    """
    visited = set()
    to_visit = [BASE_URL]
    pages = {}

    while to_visit:
        url = to_visit.pop(0)

        if url in visited:
            continue

        print(f"[crawler] Fetching: {url}")
        soup = get_page(url)

        if soup is None:
            visited.add(url)
            continue

        visited.add(url)
        pages[url] = get_text(soup)

        # Discover new links
        links = get_links(soup, url)
        for link in links:
            if link not in visited:
                to_visit.append(link)

        # Politeness window — wait before next request
        if to_visit:
            print(f"[crawler] Waiting {POLITENESS_WINDOW}s...")
            time.sleep(POLITENESS_WINDOW)

    print(f"[crawler] Done. Crawled {len(pages)} pages.")
    return pages