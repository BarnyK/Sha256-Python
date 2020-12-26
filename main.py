import argparse
from constants import INITIAL_HASH_VALUES, CONSTANTS

# Words = 32b = 4B = Unsigned Integer
# Chunk = 512b = 64B
#
def circular_shift(x: int, y: int):
    """
    Word circular shift of Word x by amount y
    Word = 4B = integer
    """
    return (((x & 0xFFFFFFFF) >> (y & 31)) | (x << (32 - (y & 31)))) & 0xFFFFFFFF


def copy_into_list(list1: list, list2: list, index: int):
    """
    Copies list2 into list1 starting from position of index
    """
    if len(list2) + index > len(list1):
        raise Exception("List length or index position mismatch")
    for i in range(len(list2)):
        list1[index + i] = list2[i]
    return list1


def pad_message(byte_message: bytearray):
    """
    Pads message to length divisible by 512b/64B
    Appends binary 1 to the message and then appends number of zeros
    Number of zeroes is chosen so that the final message is divisible by 512 in bits
    """
    message_copy = byte_message[:]  # Copy because bytearrays are passed by reference
    number_of_zeros = 64 - ((len(message_copy) + 8) & 0x3f)
    message_copy += (
        b"\x80"
        + bytearray(number_of_zeros - 1)
        + (len(message_copy)*8).to_bytes(8, "big")
    )
    return message_copy


def bytes_to_words(byte_message: bytearray):
    """
    Transforms bytearray into list of 32 bit unsigned integers
    """
    if len(byte_message) % 64 != 0:
        raise Exception("Message length must be divisible by 64B")
    result = [
        int.from_bytes(byte_message[4 * i : 4 * (i + 1)], "big")
        for i in range(int(len(byte_message) / 4))
    ]
    return result


def word_list_to_bytes(words: list):
    """
    Transforms list of words into one bytearray
    """
    result = bytes()
    for word in words:
        result += word.to_bytes(4, "big")
    return result


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


def sha256_bytes(message: bytearray):
    """
    SHA256 hashing for bytearray
    """
    rr = lambda x, y: circular_shift(x, y)  # Right Rotate
    rs = lambda x, y: (x & 0xFFFFFFFF) >> y
    s0 = lambda x: rr(x, 7) ^ rr(x, 18) ^ rs(x,3)
    s1 = lambda x: rr(x, 17) ^ rr(x, 19) ^ rs(x,10)
    S1 = lambda x: rr(x, 6) ^ rr(x, 11) ^ rr(x, 25)
    S0 = lambda x: rr(x, 2) ^ rr(x, 13) ^ rr(x, 22)
    Ch = lambda x, y, z: z ^ (x & (y ^ z))
    Maj = lambda x, y, z: ((x | y) & z) | (x & y)

    def _extend_chunk(W: list, i: int):
        return (W[i - 16] + s0(W[i - 15]) + W[i - 7] + s1(W[i - 2])) & 0xFFFFFFFF

    def _round(hash_values: tuple, w: int, c: int):
        a, b, c, d, e, f, g, h = hash_values
        T1 = h + S1(e) + Ch(e, f, g) + c + w 
        T2 = S0(a) + Maj(a, b, c)
        return (
            (T1 + T2) & 0xFFFFFFFF,
            a,
            b,
            c,
            (d + T1) & 0xFFFFFFFF,
            e,
            f,
            g,
        )

    def _hash_addition(hash1: tuple, hash2: tuple):
        return tuple([(hash1[i] + hash2[i]) & 0xFFFFFFFF for i in range(8)])

    message = pad_message(message)
    words_list = bytes_to_words(message)
    chunks = divide_message(words_list)
    hash_values = INITIAL_HASH_VALUES
    for chunk in chunks:
        W = chunk[:]
        # Extend chunks onto the whole range
        for i in range(16, 64):
            W.append(_extend_chunk(W, i))

        new_hash_values = hash_values
        for i in range(64):
            new_hash_values = _round(new_hash_values, W[i], CONSTANTS[i])

        hash_values = _hash_addition(hash_values, new_hash_values)
    return word_list_to_bytes(hash_values)


def sha256_from_file(filename):
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
    parser.add_argument("text", nargs="?", help="Text to be hashed")
    parser.add_argument(
        "--test", "-t", action="store_true", help="Runs tests for the program"
    )
    arguments = parser.parse_args()
    if arguments.test:
        print("Testing")
    elif arguments.file:
        try:
            sha256_from_file(arguments.file)
        except FileNotFoundError:
            print(f"File {arguments.file} not found")
    else:
        if arguments.text:
            print(sha256(arguments.text, "ascii").hex())
            from hashlib import sha256 as sha2562

            print(sha2562(arguments.text.encode("ascii")).hexdigest())
        else:
            print("No arguments supplied (--help for help)")
