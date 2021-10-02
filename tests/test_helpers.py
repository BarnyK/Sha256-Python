import unittest
from helpers import words_to_bytes, bytes_to_words, circular_shift


class Test_Helpers(unittest.TestCase):
    def test_bytes_to_words_values(self):
        byte_message = b"a" * 64
        words = bytes_to_words(byte_message)
        self.assertEqual(words, [1633771873] * 16)

    def test_words_to_bytes(self):
        words = [1633771873, 1633771873, 1633771873]
        byte_message = words_to_bytes(words)
        self.assertEqual(b"aaaaaaaaaaaa", byte_message)

    def test_circular_shift(self):
        self.assertEqual(circular_shift(16, 4), 1)

    def test_circular_shift_two_way(self):
        self.assertEqual(circular_shift(circular_shift(23, 4), -4), 23)
