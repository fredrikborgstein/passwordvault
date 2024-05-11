""" This module retrieves a record from the database

Returns:
    Boolean: Returns True if the record was successfully retrieved, False if the record does not exist
"""
import os
import mysql.connector
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

def retrieve_record(username, master_password, search_query):
    """Retrieves a record from the database

    Args:
        username (string): Username of the user
        master_password (string): Master password of the user
        search_query (string): The application name to search for

    Returns:
        Boolean: _description_
    """

    cursor.execute(f'USE {os.getenv("DATABASE")} ')
    cursor.execute(f'SELECT * FROM {username} WHERE application = "{search_query}";')
    record = cursor.fetchall()

    if not record:
        return False
   
    cursor.execute(f'SELECT password FROM {username} WHERE application = "{search_query}";')
    encrypted_password = cursor.fetchone()[0]
    cursor.execute(f'SELECT salt FROM {username} WHERE application = "{search_query}";')
    salt = bytes(cursor.fetchone()[0], encoding="utf-8")
    key = derive_fernet_key(bytes(master_password, encoding="utf-8"), salt)
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode("utf-8")
    cursor.execute(f'SELECT username FROM {username} WHERE application = "{search_query}";')
    app_username = cursor.fetchone()[0]
    cursor.execute(f'SELECT application FROM {username} WHERE application = "{search_query}";')
    application = cursor.fetchone()[0]

    return True, app_username, application, decrypted_password
