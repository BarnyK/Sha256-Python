import argparse
from unittest import TextTestRunner
from sys import argv
from constants import INITIAL_HASH_VALUES, CONSTANTS
from helpers import bytes_to_words, words_to_bytes, circular_shift
from test_project import make_test_suite


def pad_message(byte_message: bytes):
    """
    Pads message to length divisible by 512b/64B
    Appends binary '1' to the message and then appends number of zeros
    Instead of binary operation it appends byte with '1' in most significant bit
    and then 0 value bytes
    At the end of the message adds 64b/8B containing length(in bits) of original message
    """
    number_of_zeros = 64 - ((len(byte_message) + 8) & 0x3F) - 1
    byte_message += (
        b"\x80"
        + b"\x00" * (number_of_zeros)
        + (len(byte_message) * 8).to_bytes(8, "big")
    )
    return byte_message


def sha256(message: str, in_hex: bool = True, encoding: str = "utf-8"):
    """
    SHA256 hashing for string message
    message - string message to be hashed
    in_hex - controlls if output will be in hex(defualt) or in bytes
    encoding - specifies encoding used for string to bytes conversion
    """
    message = message.encode(encoding)
    return sha256_bytes(message, in_hex=in_hex)


def sha256_bytes(message: bytes, in_hex=True):
    """
    SHA256 hashing for bytes
    message - bytes to be hashed
    in_hex - controlls if output will be in hex or in bytes(default)
    """
    rotr = lambda x, y: circular_shift(x, y)  # Right Rotate
    rs = lambda x, y: (x & 0xFFFFFFFF) >> y  # Right Shift
    sum0 = lambda x: rotr(x, 7) ^ rotr(x, 18) ^ rs(x, 3)  # Sum 0 function
    sum1 = lambda x: rotr(x, 17) ^ rotr(x, 19) ^ rs(x, 10)  # Sum 1 function
    sigma0 = lambda x: rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)  # Sigma0 function
    sigma1 = lambda x: rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)  # Sigma1 function
    Ch = lambda x, y, z: z ^ (x & (y ^ z))  # Choose function
    Maj = lambda x, y, z: ((x | y) & z) | (x & y)  # Majority function

    def _round(hash_values: tuple, word: int, constant: int):
        # Function performing one round of the compression function
        a, b, c, d, e, f, g, h = hash_values
        temp1 = h + sigma1(e) + Ch(e, f, g) + constant + word
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

    # initializing hash value and pre-processing
    hash_values = INITIAL_HASH_VALUES
    message = pad_message(message)
    word_list = bytes_to_words(message)

    # Spltiting into 64B length chunks
    chunks = [word_list[16 * i : 16 * (i + 1)] for i in range(int(len(word_list) / 16))]
    for chunk in chunks:
        # Initializing values for the current loop
        W = chunk[:]
        current_hash_values = hash_values

        # Extend chunks onto the whole range
        for i in range(16, 64):
            W.append(
                (W[i - 16] + sum0(W[i - 15]) + W[i - 7] + sum1(W[i - 2])) & 0xFFFFFFFF
            )

        # Compression loop
        for i in range(64):
            current_hash_values = _round(current_hash_values, W[i], CONSTANTS[i])

        hash_values = tuple(
            [(current_hash_values[i] + hash_values[i]) & 0xFFFFFFFF for i in range(8)]
        )
    result = words_to_bytes(hash_values)
    if in_hex:
        return result.hex()
    else:
        return result


def sha256_from_file(filename):
    """
    Read file bytes and hashes them
    """
    with open(filename, "rb") as f:
        message = bytearray(f.read())
    return sha256_bytes(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SHA256 hashing")
    parser.add_argument(
        "--file",
        "-f",
        nargs="?",
        action="store",
        help="Allows to specify the file from which the data will be hashed",
    )
    parser.add_argument("text", nargs="?", const="", help="Text to be hashed")
    parser.add_argument(
        "--test", "-t", action="store_true", help="Runs tests for the program"
    )
    args = parser.parse_args()
    if args.test:
        # Run unittest tests
        runner = TextTestRunner(verbosity=2)
        runner.run(make_test_suite())
    elif args.file:
        try:
            print(sha256_from_file(args.file))
        except FileNotFoundError:
            print(f"File {args.file} not found")
    else:
        if args.text is not None:
            print(sha256(args.text, "ascii"))
        else:
            print("No arguments supplied (--help for help)")
