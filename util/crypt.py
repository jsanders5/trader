#!/usr/bin/env python


from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

class Crypt():
    def generate_encoded_key(pw):
        key = RSA.generate(2048)
        encoded_key = key.export_key(passphrase=pw, pkcs=8,
                                      protection="scryptAndAES128-CBC")
        return encoded_key

    def get_private_key():
        encoded_key = open("rsa_key.bin", "rb").read()
        return encoded_key

    def encrypt(data, public_key):
        # Encrypt the data public RSA key
        cipher_rsa = PKCS1_OAEP.new(public_key)
        return cipher_rsa.encrypt(data)

    def decrypt(key, enc_data):
        # Decrypt the Data with the private key
        cipher_rsa = PKCS1_OAEP.new(key)
        data = cipher_rsa.decrypt(enc_data)
        return data.decode("utf-8")


# EOF