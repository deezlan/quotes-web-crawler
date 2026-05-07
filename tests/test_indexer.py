import unittest
from src.indexer import tokenize


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


if __name__ == "__main__":
    unittest.main()