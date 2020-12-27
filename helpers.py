def bytes_to_words(byte_message: bytes, word_size: int = 4) -> list:
    """
    Transforms bytes into list of 
    """
    if len(byte_message) % word_size != 0:
        raise Exception("byte_message length should be divisible by word_size")
    result = [
        int.from_bytes(byte_message[word_size * i : word_size * (i + 1)], "big")
        for i in range(len(byte_message) // word_size)
    ]
    return result


def words_to_bytes(words: list):
    """
    Transforms list of words into one bytearray
    """
    result = bytes()
    for word in words:
        result += word.to_bytes(4, "big")
    return result


def circular_shift(x: int, y: int):
    """
    4B circular shift of Word x by amount y
    """
    return (((x & 0xFFFFFFFF) >> (y & 31)) | (x << (32 - (y & 31)))) & 0xFFFFFFFF

