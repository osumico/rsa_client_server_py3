
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import os

def encryptAES(data: str, pubkey_filename: str):
    data = data.encode("utf-8")
    file_out = open("temp_data.bin", "wb")

    recipient_key = RSA.import_key(open(f"{pubkey_filename}").read())
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
    
    file_out.close()
    with open('temp_data.bin', mode='rb') as cipher_bin:
        cipher_data = cipher_bin.read()
    
    os.remove("temp_data.bin")
    return cipher_data

def decryptAES(data: str, privkey_filename: str):
    
    data_in = open("temp_data.bin", "wb")
    data_in.write(data)
    data_in.close()
    
    bin_file = open("temp_data.bin", "rb")
    private_key = RSA.import_key(open(f"{privkey_filename}").read())

    enc_session_key, nonce, tag, ciphertext = \
    [bin_file.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    
    bin_file.close()
    os.remove("temp_data.bin")
    
    return data.decode("utf-8")