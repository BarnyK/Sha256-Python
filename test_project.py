from main import encrypt
import unittest
from hashlib import sha256


class Test_Encrypt(unittest.TestCase):
    def test_correct_encryption(self):
        self.assertEqual(
            encrypt("abcd".encode()).digest(), sha256("abcd".encode()).digest()
        )
