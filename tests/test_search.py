"""
test_search.py - Unit tests for the search module
"""

import unittest
from io import StringIO
from unittest.mock import patch
from src.search import print_index


SAMPLE_INDEX = {
    "hello": {
        "http://example.com/1": {"frequency": 2, "positions": [0, 5]},
        "http://example.com/2": {"frequency": 1, "positions": [3]}
    },
    "world": {
        "http://example.com/1": {"frequency": 1, "positions": [1]}
    }
}


class TestPrintIndex(unittest.TestCase):

    def test_prints_entry_for_known_word(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            print_index(SAMPLE_INDEX, "hello")
            output = mock_out.getvalue()
        self.assertIn("hello", output)
        self.assertIn("http://example.com/1", output)

    def test_prints_frequency(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            print_index(SAMPLE_INDEX, "hello")
            output = mock_out.getvalue()
        self.assertIn("2", output)

    def test_prints_positions(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            print_index(SAMPLE_INDEX, "hello")
            output = mock_out.getvalue()
        self.assertIn("0", output)
        self.assertIn("5", output)

    def test_word_not_in_index(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            print_index(SAMPLE_INDEX, "notaword")
            output = mock_out.getvalue()
        self.assertIn("not found", output)

    def test_empty_word(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            print_index(SAMPLE_INDEX, "")
            output = mock_out.getvalue()
        self.assertIn("No word provided", output)

    def test_case_insensitive(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            print_index(SAMPLE_INDEX, "HELLO")
            output = mock_out.getvalue()
        self.assertIn("hello", output)

    def test_whitespace_input(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            print_index(SAMPLE_INDEX, "   ")
            output = mock_out.getvalue()
        self.assertIn("No word provided", output)


if __name__ == "__main__":
    unittest.main()