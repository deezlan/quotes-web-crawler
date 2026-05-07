import unittest
import requests
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from src.crawler import get_page


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


if __name__ == "__main__":
    unittest.main()