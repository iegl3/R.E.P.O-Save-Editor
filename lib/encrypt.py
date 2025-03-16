from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad
from Crypto.Hash import HMAC, SHA1
import gzip
import os

def encrypt_es3(data, password, should_gzip=False):
    # Compress the data if required
    if should_gzip:
        data = gzip.compress(data)

    # Generate a random IV
    iv = os.urandom(16)

    # Derive the key using PBKDF2
    key = PBKDF2(password, iv, dkLen=16, count=100, prf=lambda p, s: HMAC.new(p, s, SHA1).digest())

    # Encrypt the data using AES-128-CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))

    # Prepend the IV to the encrypted data
    return iv + encrypted_data

# # Example usage
# data = input("Enter the json file path: ")
# with open(data, 'rb') as f:
#     data = f.read()
# password = "Why would you want to cheat?... :o It's no fun. :') :'D"
# encrypted_data = encrypt_es3(data, password)

# # Save the encrypted data to a file
# with open('encrypted_file.es3', 'wb') as f:
#     f.write(encrypted_data)