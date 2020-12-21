from sys import argv
from constants import *

def pad_message(byte_message: bytes):
    """
    Pads message to length divisible by 512
    Appends binary 1 to the message and then appends number of zeros
    Number of zeroes is chosen so that the final message is divisible by 512 in bits
    """
    number_of_zeros = 64 - ((len(byte_message)  + 8) % 64)
    byte_message += b'\x80' + b'\x00' * (number_of_zeros - 1)
    return byte_message


def divide_message(byte_message: bytes):
    """
    Divides messages into chunks of size 512
    """
    L = len(byte_message)
    if L % 64 != 0:
        raise Exception("Message length should be divisible by 64")
    result_messages = [byte_message[64 * i : 64 * (i+1)] for i in range(L/64)]
    return result_messages



def encrypt(message: str):
    message = message.encode("utf-8")
    print(len(message))
    return message

def encrypt_bytes(message: bytes):
    return NotImplementedError

def encrypt_file(filename):
    return NotImplementedError

if __name__ == "__main__":
    while True:
        if len(argv) == 1:
            message = input("Input data: ")
        else:
            message = argv[1]
        print(encrypt(message))
        
    
    
