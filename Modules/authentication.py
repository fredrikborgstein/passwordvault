""" This module is used to authenticate the user

    Returns:
        Boolean: returns True if the user is authenticated, False if the user is not authenticated
"""
import os
import mysql.connector
import bcrypt
from dotenv import load_dotenv

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"),
                               password=os.getenv("PASSWORD"),
                               host=os.getenv("HOST"),
                               database=os.getenv("DATABASE"),
                               charset=os.getenv("CHARSET"),
                               collation=os.getenv("COLLATION"))
cursor = conn.cursor()




def authenticate(username, password):
    """Authenticates the user

    Args:
        username (string): username of the user
        password (string): password of the user

    Returns:
        Boolean: returns True if the user is authenticated, False if the user is not authenticated
    """
    encryption_key = os.getenv("ENCRYPTION_KEY")
    cursor.execute(f'USE {os.getenv("DATABASE")} ')
    cursor.execute('''SELECT aes_decrypt(accountPassword, %s)
                   FROM master_account_records WHERE accountUsername = %s''',
                   (encryption_key, username))
    account_information = cursor.fetchone()
    if account_information:
        decrypted_password = account_information[0].decode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), decrypted_password.encode('utf-8')):
            return True
        else:
            return False
    else:
        return False
