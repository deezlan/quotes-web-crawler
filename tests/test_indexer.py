import os
import json
import tempfile
import unittest
from unittest.mock import patch
from src.indexer import tokenize, build_index, save_index, load_index


class TestTokenize(unittest.TestCase):

    def test_lowercases_text(self):
        result = tokenize("Hello World")
        self.assertEqual(result, ["hello", "world"])

    def test_strips_punctuation(self):
        result = tokenize("hello, world!")
        self.assertEqual(result, ["hello", "world"])

    def test_strips_numbers(self):
        result = tokenize("hello 123 world")
        self.assertEqual(result, ["hello", "world"])

    def test_returns_list(self):
        result = tokenize("hello")
        self.assertIsInstance(result, list)

    def test_empty_string(self):
        result = tokenize("")
        self.assertEqual(result, [])

    def test_only_punctuation(self):
        result = tokenize("!!! ??? ---")
        self.assertEqual(result, [])

    def test_preserves_multiple_words(self):
        result = tokenize("the quick brown fox")
        self.assertEqual(result, ["the", "quick", "brown", "fox"])


class TestBuildIndex(unittest.TestCase):

    def test_returns_dict(self):
        result = build_index({"http://example.com": "hello world"})
        self.assertIsInstance(result, dict)

    def test_empty_pages(self):
        result = build_index({})
        self.assertEqual(result, {})

    def test_word_appears_in_index(self):
        result = build_index({"http://example.com": "hello world"})
        self.assertIn("hello", result)

    def test_correct_frequency(self):
        result = build_index({"http://example.com": "hello hello world"})
        self.assertEqual(result["hello"]["http://example.com"]["frequency"], 2)

    def test_correct_positions(self):
        result = build_index({"http://example.com": "hello world hello"})
        self.assertEqual(result["hello"]["http://example.com"]["positions"], [0, 2])

    def test_multiple_pages(self):
        pages = {
            "http://example.com/1": "hello world",
            "http://example.com/2": "hello python"
        }
        result = build_index(pages)
        self.assertIn("http://example.com/1", result["hello"])
        self.assertIn("http://example.com/2", result["hello"])

    def test_case_insensitive(self):
        result = build_index({"http://example.com": "Hello hello HELLO"})
        self.assertEqual(result["hello"]["http://example.com"]["frequency"], 3)

    def test_word_only_on_one_page(self):
        pages = {
            "http://example.com/1": "hello world",
            "http://example.com/2": "goodbye world"
        }
        result = build_index(pages)
        self.assertNotIn("http://example.com/2", result["hello"])


class TestSaveAndLoadIndex(unittest.TestCase):

    def setUp(self):
        """Use a temporary directory for all file operations."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = os.path.join(self.temp_dir.name, "index.json")

    def tearDown(self):
        """Clean up temp directory after each test."""
        self.temp_dir.cleanup()

    @patch("src.indexer.INDEX_PATH")
    def test_save_creates_file(self, mock_path):
        mock_path.__str__ = lambda s: self.temp_path
        with patch("src.indexer.INDEX_PATH", self.temp_path):
            save_index({"hello": {}})
            self.assertTrue(os.path.exists(self.temp_path))

    @patch("src.indexer.INDEX_PATH")
    def test_save_and_load_roundtrip(self, mock_path):
        index = {"hello": {"http://example.com": {"frequency": 1, "positions": [0]}}}
        with patch("src.indexer.INDEX_PATH", self.temp_path):
            save_index(index)
            result = load_index()
            self.assertEqual(result, index)

    @patch("src.indexer.INDEX_PATH")
    def test_save_writes_valid_json(self, mock_path):
        with patch("src.indexer.INDEX_PATH", self.temp_path):
            save_index({"hello": {}})
            with open(self.temp_path, "r") as f:
                data = json.load(f)
            self.assertIsInstance(data, dict)

    @patch("src.indexer.INDEX_PATH", "/nonexistent/path/index.json")
    def test_load_returns_empty_if_no_file(self):
        result = load_index()
        self.assertEqual(result, {})

    @patch("src.indexer.INDEX_PATH")
    def test_load_returns_dict(self, mock_path):
        with patch("src.indexer.INDEX_PATH", self.temp_path):
            save_index({"word": {}})
            result = load_index()
            self.assertIsInstance(result, dict)

    @patch("src.indexer.INDEX_PATH")
    def test_save_overwrites_existing(self, mock_path):
        with patch("src.indexer.INDEX_PATH", self.temp_path):
            save_index({"old": {}})
            save_index({"new": {}})
            result = load_index()
            self.assertIn("new", result)
            self.assertNotIn("old", result)


if __name__ == "__main__":
    unittest.main()