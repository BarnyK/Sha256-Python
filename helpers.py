from typing import Sequence


def bytes_to_words(byte_message: bytes, word_size: int = 4) -> list[int]:
    """
    Transforms bytes into list of integer words
    """
    if len(byte_message) % word_size != 0:
        raise Exception("byte_message length should be divisible by word_size")
    result = [
        int.from_bytes(byte_message[word_size * i : word_size * (i + 1)], "big")
        for i in range(len(byte_message) // word_size)
    ]
    return result


def words_to_bytes(words: Sequence[int], word_size: int = 4) -> bytes:
    """
    Transforms list of words into one bytes object
    """
    return b"".join(word.to_bytes(word_size, "big") for word in words)


def circular_shift(x: int, y: int) -> int:
    """
    4 Byte circular shift of Word x by amount y
    """
    return (((x & 0xFFFFFFFF) >> (y & 31)) | (x << (32 - (y & 31)))) & 0xFFFFFFFF
