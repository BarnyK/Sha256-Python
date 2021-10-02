import unittest


class Test_Hashing(unittest.TestCase):
    def setUp(self):
        from sha256 import sha256, sha256_bytes, sha256_from_file
        from hashlib import sha256 as hashlib_sha256

        self.hash = sha256
        self.hash_bytes = sha256_bytes
        self.hash_file = sha256_from_file
        self.lib_sha256 = hashlib_sha256

    def test_against_hashlib(self):
        message = "abcd"
        hash_test = self.hash(message, "utf-8")
        hash_known = self.lib_sha256(message.encode("utf-8")).hexdigest()
        self.assertEqual(hash_test, hash_known)

    def test_against_hashlib_non_ascii(self):
        message = "łźśąęąęóajiojsdiaofjdoikasg"
        hash_test = self.hash(message, "utf-8")
        hash_known = self.lib_sha256(message.encode("utf-8")).hexdigest()
        self.assertEqual(hash_test, hash_known)

    def test_against_hashlib_very_long(self):
        message = "abc" * 10000
        hash_test = self.hash(message, "utf-8")
        hash_known = self.lib_sha256(message.encode("utf-8")).hexdigest()
        self.assertEqual(hash_test, hash_known)

    def test_bytes_hashing(self):
        message = b"asdf"
        hash_test = self.hash_bytes(message)
        hash_known = self.lib_sha256(message).hexdigest()
        self.assertEqual(hash_test, hash_known)

    def test_bytes_hashing_very_big(self):
        message = b"\xFF" * 300
        hash_test = self.hash_bytes(message)
        hash_known = self.lib_sha256(message).hexdigest()
        self.assertEqual(hash_test, hash_known)

    def test_known_empty(self):
        # source: https://en.wikipedia.org/wiki/SHA-2
        hash_test = self.hash("")
        self.assertEqual(
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            hash_test,
        )

    def test_known_abc(self):
        # source: https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/SHA256.pdf
        hash_test = self.hash("abc")
        self.assertEqual(
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            hash_test,
        )

    def test_known_longer(self):
        # source: https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/SHA256.pdf
        hash_test = self.hash(
            "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
        )
        self.assertEqual(
            "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1",
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

