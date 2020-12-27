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


def circular_shift(x: int, y: int):
    """
    Word circular shift of Word x by amount y
    Word = 4B = integer
    """
    return (((x & 0xFFFFFFFF) >> (y & 31)) | (x << (32 - (y & 31)))) & 0xFFFFFFFF
