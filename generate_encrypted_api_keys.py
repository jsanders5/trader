from Crypto.PublicKey import RSA
from util.crypt import Crypt
from pwinput import pwinput

RSA_KEY_FILE_NAME = "crypt/rsa_key.bin"
ENC_KEY_FILE_NAME = "crypt/encrypted_key.bin"
ENC_SECRET_FILE_NAME = "crypt/encrypted_secret.bin"

def get_encoded_key():
    encoded_key = open(RSA_KEY_FILE_NAME, "rb").read()
    return encoded_key

def get_data(filename):
    enc_data = open(filename, "rb").read()
    return enc_data

def store_data(filename, encrypted_data):
    file_out = open(filename, "wb")
    file_out.write(encrypted_data)
    file_out.close()

def decrypt_binary_file(filename, private_key):
    enc_data = get_data(filename)
    return Crypt.decrypt(private_key, enc_data)

def get_user_input(prompt):
    input = pwinput(prompt)
    return input.encode("utf-8")

def encrypt_keys():
    print("Generating encrypted API keys...")
    password = pwinput("Enter Password: ")

    encoded_key = Crypt.generate_encoded_key(password)
    store_data(RSA_KEY_FILE_NAME, encoded_key)

    key_data_utf8 = get_user_input("Enter key: \t")

    private_key = RSA.import_key(encoded_key, passphrase=password)
    public_key = private_key.public_key()

    encrypted_data = Crypt.encrypt(key_data_utf8, public_key)
    store_data(ENC_KEY_FILE_NAME, encrypted_data)

    secret_data_utf8 = get_user_input("Enter Secret: \t")

    encrypted_data = Crypt.encrypt(secret_data_utf8, public_key)

    store_data(ENC_SECRET_FILE_NAME, encrypted_data)

def decrypt_keys():
    print("Decrypting API keys...")
    password = pwinput("Enter Password: ")

    # Read encoded_key from file
    encoded_key = get_encoded_key()

    # Derive private key
    try:
        private_key = RSA.import_key(encoded_key, passphrase=password)
    except ValueError:
        print("You password was incorrect - Don't test me!")
        quit()

    # Decrypt binary file
    decrypted_key = decrypt_binary_file(ENC_KEY_FILE_NAME, private_key)
#     print("key: ", decrypted_data)

    decrypted_secret = decrypt_binary_file(ENC_SECRET_FILE_NAME, private_key)
#     print("secret: ", decrypted_data)
    return decrypted_key, decrypted_secret

def main():
    encrypt_keys()
    decrypt_keys()


if __name__== "__main__":
  main()


# EOF