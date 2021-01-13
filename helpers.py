def bytes_to_words(byte_message: bytes, word_size: int = 4):
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


def words_to_bytes(words: list, word_size: int = 4):
    """
    Transforms list of words into one bytes object
    """
    result = bytes()
    for word in words:
        result += word.to_bytes(word_size, "big")
    return result


def circular_shift(x: int, y: int):
    """
    4 Byte circular shift of Word x by amount y
    """
    return (((x & 0xFFFFFFFF) >> (y & 31)) | (x << (32 - (y & 31)))) & 0xFFFFFFFF

