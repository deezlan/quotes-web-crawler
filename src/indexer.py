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