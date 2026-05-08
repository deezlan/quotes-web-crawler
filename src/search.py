"""
search.py - Search functionality for the inverted index.

Provides print and find operations against a loaded inverted index.
"""


def print_index(index: dict, word: str) -> None:
    """
    Print the inverted index entry for a given word.
    Shows all pages the word appears in, with frequency and positions.
    """
    word = word.lower().strip()

    if not word:
        print("[search] No word provided.")
        return

    if word not in index:
        print(f"[search] '{word}' not found in index.")
        return

    entries = index[word]
    print(f"\nIndex entries for '{word}':")
    for url, stats in entries.items():
        print(f"  {url}")
        print(f"    Frequency : {stats['frequency']}")
        print(f"    Positions : {stats['positions']}")


def find_pages(index: dict, query: str) -> list[str]:
    """
    Find all pages containing every word in the query.
    Returns a list of URLs where all query words appear.
    Multi-word queries use AND logic — all words must be present.
    """
    words = query.lower().strip().split()

    if not words:
        print("[search] No query provided.")
        return []

    # Find pages for each word, handle words not in index
    results = None
    for word in words:
        if word not in index:
            print(f"[search] '{word}' not found in index.")
            return []

        pages = set(index[word].keys())
        results = pages if results is None else results & pages

    if not results:
        print("[search] No pages found matching all query terms.")
        return []

    matches = sorted(results)
    print(f"\nPages matching '{query}':")
    for url in matches:
        print(f"  {url}")

    return matches