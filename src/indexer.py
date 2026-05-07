"""
Takes raw page text from the crawler and produces an inverted index
mapping each word to the pages it appears in, with frequency and positions.
"""

import re
import json
import os

INDEX_PATH = os.path.join("data", "index.json")


def tokenize(text: str) -> list[str]:
    """
    Convert raw text into a list of clean, lowercase tokens.
    Strips punctuation and ignores empty strings.
    """
    text = text.lower()
    tokens = re.findall(r'\b[a-z]+\b', text)
    return tokens


def build_index(pages: dict[str, str]) -> dict:
    """
    Build an inverted index from crawled pages.
    
    Takes a dict of {url: raw_text} and returns an inverted index:
    {
        "word": {
            "url": {
                "frequency": 3,
                "positions": [0, 5, 12]
            }
        }
    }
    """
    index = {}

    for url, text in pages.items():
        tokens = tokenize(text)

        for position, word in enumerate(tokens):
            if word not in index:
                index[word] = {}

            if url not in index[word]:
                index[word][url] = {"frequency": 0, "positions": []}

            index[word][url]["frequency"] += 1
            index[word][url]["positions"].append(position)

    return index


def save_index(index: dict) -> None:
    """
    Save the inverted index to disk as a JSON file.
    """
    os.makedirs("data", exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    print(f"[indexer] Index saved to {INDEX_PATH}")


def load_index() -> dict:
    """
    Load the inverted index from disk.
    Returns an empty dict if no index file exists.
    """
    if not os.path.exists(INDEX_PATH):
        print("[indexer] No index file found. Run 'build' first.")
        return {}
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index = json.load(f)
    print(f"[indexer] Index loaded from {INDEX_PATH}")
    return index