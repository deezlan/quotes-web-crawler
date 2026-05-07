"""
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