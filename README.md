# COMP3011 Search Engine

A command-line search engine that crawls [quotes.toscrape.com](https://quotes.toscrape.com/), builds an inverted index, and supports search queries.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/main.py
```

Then use the following commands in the shell:

| Command | Description |
|---|---|
| `build` | Crawl the website and build the index |
| `load` | Load a previously built index from disk |
| `print <word>` | Print the index entry for a word |
| `find <word(s)>` | Find all pages containing the search terms |

## Testing

```bash
python -m pytest tests/
```

## Dependencies

- `requests` — HTTP requests for crawling
- `beautifulsoup4` — HTML parsing