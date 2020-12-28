import unittest


class Test_Hashing(unittest.TestCase):
    def setUp(self):
        from sha256 import sha256, sha256_bytes, sha256_from_file
        from hashlib import sha256 as hashlib_sha256

        self.hash = sha256
        self.hash_bytes = sha256_bytes
        self.hash_file = sha256_from_file
        self.lib_sha256 = hashlib_sha256

    def test_result_against_hashlib(self):
        message = "abcd"
        hash_test = self.hash(message, "utf-8")
        hash_known = self.lib_sha256(message.encode("utf-8")).hexdigest()
        self.assertEqual(hash_test, hash_known)

        message = "łźśąęąęóajiojsdiaofjdoikasg"
        hash_test = self.hash(message, "utf-8")
        hash_known = self.lib_sha256(message.encode("utf-8")).hexdigest()
        self.assertEqual(hash_test, hash_known)

        message = "r9VrOyhZDCzZ2iYMXhwl"
        hash_test = self.hash(message, "utf-8")
        hash_known = self.lib_sha256(message.encode("utf-8")).hexdigest()
        self.assertEqual(hash_test, hash_known)

        message = "OMqzk0wbdU4JeleDey8f"
        hash_test = self.hash(message, "utf-8")
        hash_known = self.lib_sha256(message.encode("utf-8")).hexdigest()
        self.assertEqual(hash_test, hash_known)

    def test_very_long(self):
        message = "abc" * 10000
        hash_test = self.hash(message, "utf-8")
        hash_known = self.lib_sha256(message.encode("utf-8")).hexdigest()
        self.assertEqual(hash_test, hash_known)

    def test_very_big(self):
        message = b"\xFF" * 300
        hash_test = self.hash_bytes(message)
        hash_known = self.lib_sha256(message).hexdigest()
        self.assertEqual(hash_test, hash_known)

    def test_result_empty(self):
        hash_test = self.hash("")
        self.assertEqual(
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            hash_test,
        )

    def test_file_hashing(self):
        from os import remove

        message = b"abcd"
        with open("test_file.tmp", "wb") as f:
            f.write(message)
        hash_known = self.lib_sha256(message).hexdigest()
        hash_file = self.hash_file("test_file.tmp")
        self.assertEqual(hash_known, hash_file)
        remove("test_file.tmp")


class Test_Padding(unittest.TestCase):
    def setUp(self):
        from sha256 import pad_message

        self.pad_message = pad_message

    def test_padding(self):
        message = bytearray("abcd", "utf-8")
        padded_message = self.pad_message(message)
        message += b"\x80" + b"\x00" * 58 + b"\x20"
        self.assertEqual(padded_message, message)

    def test_padding_for_empty(self):
        message = bytearray()
        padded_message = self.pad_message(message)
        message += b"\x80" + b"\x00" * 63
        self.assertEqual(padded_message, message)

    def test_padding_for_big(self):
        message = bytearray("a" * 534, "utf-8")
        padded_message = self.pad_message(message)
        message += b"\x80" + b"\x00" * 33 + b"\x00\x00\x00\x00\x00\x00\x10\xb0"
        self.assertEqual(padded_message, message)

    def test_padding_for_length(self):
        message = bytearray("a" * 534, "utf-8")
        padded_message = self.pad_message(message)
        self.assertEqual(len(padded_message), 576)


class Test_Helpers(unittest.TestCase):
    def test_bytes_to_words_values(self):
        from helpers import bytes_to_words

        byte_message = b"a" * 64
        words = bytes_to_words(byte_message)
        self.assertEqual(words, [1633771873] * 16)

    def test_words_to_bytes(self):
        from helpers import words_to_bytes

        words = [1633771873, 1633771873, 1633771873]
        byte_message = words_to_bytes(words)
        self.assertEqual(b"aaaaaaaaaaaa", byte_message)

    def test_circular_shift(self):
        from helpers import circular_shift

        self.assertEqual(circular_shift(16, 4), 1)

    def test_circular_shift_two_way(self):
        from helpers import circular_shift

        self.assertEqual(circular_shift(circular_shift(23, 4), -4), 23)


def make_test_suite():
    loader = unittest.TestLoader()
    suite = loader.discover("", pattern="test_*.py")
    return suite


if __name__ == "__main__":
    unittest.main()