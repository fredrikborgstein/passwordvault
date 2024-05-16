""" A collection of utility functions for the application.
"""
import os
import mysql.connector
from mysql.connector import Error
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import bcrypt
from dotenv import load_dotenv, dotenv_values, set_key


def get_account_id(username):
    try:
        load_dotenv()
        conn = mysql.connector.connect(user=os.getenv("USER"),
                                       password=os.getenv("PASSWORD"),
                                       host=os.getenv("HOST"),
                                       database=os.getenv("DATABASE"),
                                       charset=os.getenv("CHARSET"),
                                       collation=os.getenv("COLLATION"))
        cursor = conn.cursor()
        search_query = '''SELECT accountID FROM master_accounts
                        WHERE accountUsername = %s'''
        cursor.execute(search_query, (username,))
        account_records = cursor.fetchone()
        account_id = account_records[0]
        return account_id
    except Error as e:
        print(f'An error has occured {e}')
        return False
    finally:
        cursor.close()
        conn.close()


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


def set_encryption_key():
    new_encryption_key = bcrypt.gensalt(26).decode('utf-8')
    env_vars = dotenv_values('.env')
    env_vars['ENCRYPTION_KEY'] = new_encryption_key

    for key, value in env_vars.items():
        set_key('.env', key, value)

    return True
