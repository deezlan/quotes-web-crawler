"""
test_crawler.py - Unit tests for the crawler module.
"""

import unittest
import requests
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from src.crawler import get_page, get_links, get_text, crawl, BASE_URL


class TestGetPage(unittest.TestCase):

    @patch("src.crawler.requests.get")
    def test_returns_soup_on_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><body><p>Hello</p></body></html>"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = get_page("https://quotes.toscrape.com")
        self.assertIsInstance(result, BeautifulSoup)

    @patch("src.crawler.requests.get")
    def test_returns_none_on_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network error")
        result = get_page("https://quotes.toscrape.com")
        self.assertIsNone(result)


class TestGetLinks(unittest.TestCase):

    def _make_soup(self, html):
        return BeautifulSoup(html, "html.parser")

    def test_extracts_internal_links(self):
        soup = self._make_soup('<a href="/page/2/">Next</a>')
        links = get_links(soup, BASE_URL)
        self.assertIn("https://quotes.toscrape.com/page/2/", links)

    def test_ignores_external_links(self):
        soup = self._make_soup('<a href="https://external.com/page">External</a>')
        links = get_links(soup, BASE_URL)
        self.assertEqual(links, [])

    def test_returns_empty_for_no_links(self):
        soup = self._make_soup("<p>No links here</p>")
        links = get_links(soup, BASE_URL)
        self.assertEqual(links, [])

    def test_converts_relative_to_absolute(self):
        soup = self._make_soup('<a href="/tag/love/">Love</a>')
        links = get_links(soup, BASE_URL)
        self.assertIn("https://quotes.toscrape.com/tag/love/", links)


class TestGetText(unittest.TestCase):

    def test_extracts_visible_text(self):
        soup = BeautifulSoup("<p>Hello world</p>", "html.parser")
        text = get_text(soup)
        self.assertIn("Hello world", text)

    def test_strips_script_tags(self):
        soup = BeautifulSoup("<script>alert('x')</script><p>Real</p>", "html.parser")
        text = get_text(soup)
        self.assertNotIn("alert", text)
        self.assertIn("Real", text)

    def test_strips_style_tags(self):
        soup = BeautifulSoup("<style>.x { color: red }</style><p>Visible</p>", "html.parser")
        text = get_text(soup)
        self.assertNotIn("color", text)
        self.assertIn("Visible", text)

    def test_returns_string(self):
        soup = BeautifulSoup("<p>Text</p>", "html.parser")
        self.assertIsInstance(get_text(soup), str)


class TestCrawl(unittest.TestCase):

    @patch("src.crawler.time.sleep")
    @patch("src.crawler.get_page")
    def test_crawl_returns_dict(self, mock_get_page, mock_sleep):
        soup = BeautifulSoup("<html><body><p>Quote</p></body></html>", "html.parser")
        mock_get_page.return_value = soup
        result = crawl()
        self.assertIsInstance(result, dict)

    @patch("src.crawler.time.sleep")
    @patch("src.crawler.get_page")
    def test_crawl_respects_politeness(self, mock_get_page, mock_sleep):
        # Two pages: home links to /page/2/, /page/2/ has no links
        def fake_get_page(url):
            if url == BASE_URL:
                return BeautifulSoup(
                    '<a href="/page/2/">Next</a>', "html.parser"
                )
            return BeautifulSoup("<p>Last page</p>", "html.parser")

        mock_get_page.side_effect = fake_get_page
        crawl()
        mock_sleep.assert_called_with(6)

    @patch("src.crawler.time.sleep")
    @patch("src.crawler.get_page")
    def test_crawl_skips_failed_pages(self, mock_get_page, mock_sleep):
        mock_get_page.return_value = None
        result = crawl()
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)

    @patch("src.crawler.time.sleep")
    @patch("src.crawler.get_page")
    def test_crawl_does_not_revisit_pages(self, mock_get_page, mock_sleep):
        # Page links to itself — should only be visited once
        soup = BeautifulSoup(
            f'<a href="{BASE_URL}">Home</a>', "html.parser"
        )
        mock_get_page.return_value = soup
        crawl()
        mock_get_page.assert_called_once()


if __name__ == "__main__":
    unittest.main()