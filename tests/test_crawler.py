import unittest
import requests
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from src.crawler import get_page, get_links, BASE_URL


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


if __name__ == "__main__":
    unittest.main()