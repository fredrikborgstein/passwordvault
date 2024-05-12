"""This module lists all records for the user
"""
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from Modules.utilities import derive_fernet_key

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"),
                               password=os.getenv("PASSWORD"),
                               host=os.getenv("HOST"),
                               database=os.getenv("DATABASE"),
                               charset=os.getenv("CHARSET"),
                               collation=os.getenv("COLLATION"))
cursor = conn.cursor()

def list_all_records(username, master_password):
    """Lists all records for the user

    Args:
        username (string): The username of the user
        master_password (string): The master password of the user
    """
    try:
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        cursor.execute(f'SELECT * FROM {username};')
        record = cursor.fetchall()

        for l in record:
            application_name = l[2]
            application_username = l[1]
            application_encrypted_password = l[3]
            application_salt = l[4]
            salt = bytes(application_salt, encoding="utf-8")
            key = derive_fernet_key(bytes(master_password, encoding="utf-8"), salt)
            f = Fernet(key)
            decrypted_password = f.decrypt(application_encrypted_password).decode("utf-8")
            print("-" * 50)
            print(f"Application: {application_name}")
            print(f"Username: {application_username}")
            print(f"Password: {decrypted_password}")

    except Error as error:
        print("Error", "An error has occured: ", error)
    finally:
        cursor.close()
        conn.close()
