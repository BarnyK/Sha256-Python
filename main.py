import argparse
from constants import INITIAL_HASH_VALUES, CONSTANTS

# Words = 32b
def circular_shift(x: bytes, y: int):
    """
    Word circular shift of bytes x by amount y
    """
    x = int.from_bytes(x, "big")
    return NotImplementedError


def xor(x: bytearray, y: bytearray):
    """
    XOR for bytes type
    """
    if len(x) != len(y):
        raise Exception("XOR arguments should be the same length")
    return bytes(int.from_bytes(x, "big") ^ int.from_bytes(y, "big"))


def pad_message(byte_message: bytearray):
    """
    Pads message to length divisible by 512
    Appends binary 1 to the message and then appends number of zeros
    Number of zeroes is chosen so that the final message is divisible by 512 in bits
    """
    message_copy = byte_message[:] # Copy because bytearrays are done
    number_of_zeros = 64 - ((len(message_copy) + 8) % 64)
    message_copy += b"\x80" + bytearray(number_of_zeros - 1) + (len(message_copy)).to_bytes(8,"big")
    return message_copy


def divide_message(byte_message: bytearray):
    """
    Divides messages into chunks of size 512
    """
    L = len(byte_message)
    if L % 64 != 0:
        raise Exception("Message length should be divisible by 64")
    result_messages = [byte_message[64 * i : 64 * (i + 1)] for i in range(int(L / 64))]
    return result_messages


def sha256(message: str, encoding:str = "utf-8"):
    message = bytearray(message, encoding)
    return sha256_bytes(message)


def sha256_bytes(message: bytes):
    message = pad_message(message)
    messages = divide_message(message)
    hash_values = INITIAL_HASH_VALUES
    for m in messages:
        chunk = m
        for i in range(16,64):
            i
    print(len(message))
    return NotImplementedError


def sha256_from_file(filename):
    with open(filename, "rb") as f:
        message = f.read()
    return sha256_bytes(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SHA256 hashing")
    parser.add_argument("--file", "-f" , nargs="?", action="store")
    parser.add_argument("text", nargs="?", help="Text to be hashed")
    arguments = parser.parse_args()
    if arguments.file:
        try:
            sha256_from_file(arguments.file)
        except FileNotFoundError:
            print(f"File {arguments.file} not found")
    else:
        if arguments.text:
            print(sha256(arguments.text))
        else:
            print("No arguments supplied (--help for help)")
