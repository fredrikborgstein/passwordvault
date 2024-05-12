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


def authentication(username, password):

    encryption_key = os.getenv("ENCRYPTION_KEY")
    cursor.execute(f'USE {os.getenv("DATABASE")}')
    id_query = 'SELECT accountID, accountUsername FROM master_accounts WHERE accountUsername = %s'
    cursor.execute(id_query, (username,))
    account_records = cursor.fetchall()
    if account_records:
        account_id = account_records[0][0]
        pass_qury = '''SELECT aes_decrypt(hashedPassword,%s)
                       FROM password_hashes WHERE accountID = %s'''
        cursor.execute(pass_qury, (encryption_key, account_id))
        encrypted_password = cursor.fetchone()
        decrypted_password = encrypted_password[0].decode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), decrypted_password.encode('utf-8')):
            return True
        else:
            return False
    else:
        return False
