import unittest


class Test_Hashing(unittest.TestCase):
    def setUp(self):
        from main import sha256

        self.hash = sha256

    def test_result_against_hashlib(self):
        from hashlib import sha256

        message = "mzxkjcvnjkznxjkgvneqwiufhqwpqmajsdklfmaklsdmflkmklni2h543245njk"
        hash_test = self.hash(message)
        hash_known = sha256(message)
        self.assertEqual(hash_test, hash_known)


class Test_Padding(unittest.TestCase):
    def setUp(self):
        from main import pad_message

        self.pad_message = pad_message

    def test_padding(self):
        message = bytearray("abcd","utf-8")
        padded_message = self.pad_message(message)
        message += b"\x80" + b"\x00" * 58 + b"\x04"
        self.assertEqual(padded_message, message)

    def test_padding_for_empty(self):
        message = bytearray()
        padded_message = self.pad_message(message)
        message += b"\x80" + b"\x00" * 63 
        self.assertEqual(padded_message, message)

    def test_padding_for_big(self):
        message = bytearray("a" * 534,"utf-8")
        padded_message = self.pad_message(message)
        message += b"\x80" + b"\x00" * 33 + b"\x00\x00\x00\x00\x00\x00\x02\x16"
        print(len(message))
        print(len(padded_message))
        self.assertEqual(padded_message, message)

    def test_padding_for_length(self):
        message = bytearray("a" * 534,"utf-8")
        padded_message = self.pad_message(message)
        self.assertEqual(len(padded_message), 576)



class Test_Message_Division(unittest.TestCase):
    def setUp(self):
        from main import divide_message

        self.divide = divide_message

    def test_exception(self):
        message = b"a" * 63
        self.assertRaises(Exception, self.divide, message)

    def test_correct_number(self):
        message = b"a" * 64 * 5
        messages = self.divide(message)
        self.assertEqual(len(messages), 5)

    def test_correct_lengths(self):
        message = b"a" * 64 * 5
        messages = self.divide(message)
        for m in messages:
            self.assertEquals(len(m), 64)

    def test_correct_result(self):
        message = b"a" * 64 * 64
        messages = self.divide(message)
        res_message = b"".join(messages)
        self.assertEquals(res_message, message)
