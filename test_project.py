import unittest


class Test_Encryption(unittest.TestCase):

    def setUp(self):
        from main import encrypt
        self.encrypt = encrypt

    def test_result_against_hashlib(self):
        from hashlib import sha256
        message = "mzxkjcvnjkznxjkgvneqwiufhqwpqmajsdklfmaklsdmflkmklni2h543245njk"
        encrypted_test = self.encrypt(message)
        encrypted_known = sha256(message)
        self.assertEqual(
            encrypted_test, encrypted_known
        )
class Test_Padding(unittest.TestCase):

    def setUp(self):
        from main import pad_message
        self.pad_message = pad_message

    def test_correct_padding(self):
        message = b'abcd'
        padded_message = self.pad_message(message)
        message += b'\x80' + b'\x00' * 51
        self.assertEqual(padded_message, message)

    def test_correct_padding_for_empty(self):
        message = b""
        padded_message = self.pad_message(message)
        message = b'\x80' + b'\x00' * 55
        self.assertEqual(padded_message, message)

    def test_correct_padding_for_big(self):
        message = b"a" * 534
        padded_message = self.pad_message(message)
        message += b'\x80' + b'\x00' * 33
        self.assertEqual(padded_message, message)