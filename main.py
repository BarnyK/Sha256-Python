from hashlib import sha256

def encrypt(data):
    return sha256(data)