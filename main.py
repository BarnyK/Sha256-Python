import argparse
from sys import argv
from constants import INITIAL_HASH_VALUES, CONSTANTS
from helpers import bytes_to_words, words_to_bytes, circular_shift


def pad_message(byte_message: bytes):
    """
    Pads message to length divisible by 512b/64B
    Appends binary 1 to the message and then appends number of zeros
    Number of zeroes is chosen so that the final message is divisible by 512 in bits
    """
    message_copy = byte_message[:]  # Copy because bytearrays are passed by reference
    number_of_zeros = 64 - ((len(message_copy) + 8) & 0x3F)
    message_copy += (
        b"\x80"
        + bytearray(number_of_zeros - 1)
        + (len(message_copy) * 8).to_bytes(8, "big")
    )
    return message_copy


def divide_message(word_list: list):
    """
    Takes in list of words
    Divides messages into chunks of size 16W/64B/512b
    """
    L = len(word_list)
    if L % 16 != 0:
        raise Exception("Word list length should be divisible by 16")
    result_messages = [word_list[16 * i : 16 * (i + 1)] for i in range(int(L / 16))]
    return result_messages


def sha256(message: str, encoding: str = "utf-8"):
    message = bytearray(message, encoding)
    return sha256_bytes(message)


def sha256_bytes(message: bytes):
    """
    SHA256 hashing for bytearray
    """
    rotr = lambda x, y: circular_shift(x, y)                # Right Rotate
    rs = lambda x, y: (x & 0xFFFFFFFF) >> y                 # Right Shift
    sum0 = lambda x: rotr(x, 7) ^ rotr(x, 18) ^ rs(x, 3)      # Sum 0 function
    sum1 = lambda x: rotr(x, 17) ^ rotr(x, 19) ^ rs(x, 10)    # Sum 1 function
    sigma0 = lambda x: rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)   # Sigma0 function
    sigma1 = lambda x: rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)   # Sigma1 function
    Ch = lambda x, y, z: z ^ (x & (y ^ z))                  # Choose function
    Maj = lambda x, y, z: ((x | y) & z) | (x & y)           # Majority function

    def _round(hash_values: tuple, w: int, constant: int):
        # Function performing one round of the compression function
        a, b, c, d, e, f, g, h = hash_values
        temp1 = h + sigma1(e) + Ch(e, f, g) + constant + w
        temp2 = sigma0(a) + Maj(a, b, c)
        return (
            (temp1 + temp2) & 0xFFFFFFFF,
            a,
            b,
            c,
            (d + temp1) & 0xFFFFFFFF,
            e,
            f,
            g,
        )

    message = pad_message(message)
    words_list = bytes_to_words(message)
    chunks = divide_message(words_list)
    hash_values = INITIAL_HASH_VALUES
    for chunk in chunks:
        W = chunk[:]
        # Extend chunks onto the whole range
        for i in range(16, 64):
            W.append((W[i - 16] + sum0(W[i - 15]) + W[i - 7] + sum1(W[i - 2])) & 0xFFFFFFFF)

        new_hash_values = hash_values
        for i in range(64):
            new_hash_values = _round(new_hash_values, W[i], CONSTANTS[i])

        hash_values = tuple([(new_hash_values[i] + hash_values[i]) & 0xFFFFFFFF for i in range(8)])
    return words_to_bytes(hash_values)


def sha256_from_file(filename):
    with open(filename, "rb") as f:
        message = bytearray(f.read())
    return sha256_bytes(message)


def make_test_suite():
    loader = unittest.TestLoader()
    suite = loader.discover("", pattern="test_*.py")

    return suite


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SHA256 hashing")
    parser.add_argument(
        "--file",
        "-f",
        nargs="?",
        action="store",
        help="Allows to specify the file from which the data will be hashed",
    )
    parser.add_argument("text", nargs="?", help="Text to be hashed")
    parser.add_argument(
        "--test", "-t", action="store_true", help="Runs tests for the program"
    )
    args = parser.parse_args()
    if args.test:
        import unittest

        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(make_test_suite())
    elif args.file:
        try:
            sha256_from_file(args.file)
        except FileNotFoundError:
            print(f"File {args.file} not found")
    else:
        if args.text:
            print(sha256(args.text, "ascii").hex())
            from hashlib import sha256 as sha2562

            print(sha2562(args.text.encode("ascii")).hexdigest())
        else:
            print("No arguments supplied (--help for help)")
