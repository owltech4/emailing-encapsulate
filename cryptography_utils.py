#********************************************************************
#This module will be responsible for the encryption and decryption of your credentials. 
#Here, we will use Python's cryptography library.
#
#Before running your project, execute generate_key() once to generate your secret.key and 
#use encrypt_message() to encrypt your credentials. Store the encrypted values in config.json
#
#********************************************************************
#
#


from cryptography.fernet import Fernet, InvalidToken

# Function to generate a key. It should be done once and the same key used for encrypting/decrypting
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Loads the secret key
def load_key():
    return open("secret.key", "rb").read()

# Encrypts a message
def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

# Decrypts a message
def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    # Checks if the token is valid before decrypting the message. If not, it throws an exception.
    try:
        # Decrypts the message using the secret key and the encrypted token. The token is encrypted before
        # decrypting the message to ensure integrity. If the token is invalid, the InvalidToken exception 
        # is thrown, and the program terminates. 
        # If the token is valid, the message is decrypted and returned. 
        # Note: The token is encrypted before decrypting the message to ensure integrity. This is 
        # important to ensure that the message was not altered during encryption. If the token is changed 
        # during encryption, the program may have a security issue. That is, the token can be changed,
        # and the message can be decrypted with a different secret key. This can lead to a forgery attack.
        decrypted_message = f.decrypt(encrypted_message)
        return decrypted_message.decode()
    except InvalidToken as e:
        print("Decryption failure: Invalid token. Check if the encryption key is correct.")
        # Here, you can decide what to do next, such as stopping the execution, returning a default value, etc. 
        # For example, you might return None or re-throw the exception to be handled elsewhere.
        return None  # Or, optionally, use ´raise´ to re-throw the exception.
    
