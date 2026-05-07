"""
test_search.py - Unit tests for the search module
"""

import unittest
from io import StringIO
from unittest.mock import patch
from src.search import print_index, find_pages


SAMPLE_INDEX = {
    "hello": {
        "http://example.com/1": {"frequency": 2, "positions": [0, 5]},
        "http://example.com/2": {"frequency": 1, "positions": [3]}
    },
    "world": {
        "http://example.com/1": {"frequency": 1, "positions": [1]}
    },
    "goodbye": {
        "http://example.com/2": {"frequency": 1, "positions": [0]}
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


class TestFindPages(unittest.TestCase):

    def test_returns_list(self):
        result = find_pages(SAMPLE_INDEX, "hello")
        self.assertIsInstance(result, list)

    def test_single_word_match(self):
        result = find_pages(SAMPLE_INDEX, "hello")
        self.assertIn("http://example.com/1", result)
        self.assertIn("http://example.com/2", result)

    def test_multi_word_and_logic(self):
        # "hello" is on /1 and /2, "world" is only on /1
        result = find_pages(SAMPLE_INDEX, "hello world")
        self.assertEqual(result, ["http://example.com/1"])

    def test_no_match_returns_empty(self):
        # "hello" on /1 and /2, "goodbye" only on /2, "world" only on /1
        result = find_pages(SAMPLE_INDEX, "world goodbye")
        self.assertEqual(result, [])

    def test_word_not_in_index(self):
        result = find_pages(SAMPLE_INDEX, "notaword")
        self.assertEqual(result, [])

    def test_empty_query(self):
        result = find_pages(SAMPLE_INDEX, "")
        self.assertEqual(result, [])

    def test_case_insensitive(self):
        result = find_pages(SAMPLE_INDEX, "HELLO")
        self.assertIn("http://example.com/1", result)

    def test_whitespace_query(self):
        result = find_pages(SAMPLE_INDEX, "   ")
        self.assertEqual(result, [])

    def test_returns_sorted(self):
        result = find_pages(SAMPLE_INDEX, "hello")
        self.assertEqual(result, sorted(result))

    def test_partial_match_not_returned(self):
        # "world" not on /2, so /2 should not appear
        result = find_pages(SAMPLE_INDEX, "hello world")
        self.assertNotIn("http://example.com/2", result)


if __name__ == "__main__":
    unittest.main()