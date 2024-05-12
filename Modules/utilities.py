""" A collection of utility functions for the application.
"""
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import bcrypt


def create_fernet_key(password):
    """_summary_

    Args:
        password (string): The password to be used to create the key

    Returns:
        string: Returns a key and salt for the Fernet encryption
    """
    salt = bcrypt.gensalt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key, salt



def derive_fernet_key(password, salt):
    """Returns a recreation of the key for the Fernet encryption

    Args:
        password (string): The password to be used to recreate the key
        salt (string): The salt to be used to recreate the key

    Returns:
        _type_: The key for the Fernet encryption
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def derive_salt(db_salt):
    """_summary_

    Args:
        db_salt (string): The salt to be used to recreate the key

    Returns:
        string: The salt for the Fernet encryption
    """
    salt = bytes(db_salt, encoding="utf-8")
    return salt
