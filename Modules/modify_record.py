"""This module is used to modify a record in the database

Returns:
    Boolean: Returns True if the record was
                successfully modified, False if the record does not exist
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from Modules.utilities import create_fernet_key

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"),
                               password=os.getenv("PASSWORD"),
                               host=os.getenv("HOST"),
                               database=os.getenv("DATABASE"),
                               charset=os.getenv("CHARSET"),
                               collation=os.getenv("COLLATION"))
cursor = conn.cursor()


def modify_record(username, master_password,
                  record_to_modify,
                  new_application_name,
                  new_application_username,
                  new_application_password):
    """Modifies a record in the database

    Args:
        username (string): The username of the user
        master_password (string): The master password of the user
        record_to_modify (string): The name of the application to be modified
        new_application_name (string): The new name for the application being modified
        new_application_username (string): The new username for the application being modified
        new_application_password (string): The new password for the application being modified

    Returns:
        Boolean: Returns True if the record was
        successfully modified, False if the record does not exist
    """

    try:
        cursor.execute(f'DELETE FROM {username} WHERE application = "{record_to_modify}";')

        key, salt = create_fernet_key(bytes(master_password, encoding="utf-8"))
        f = Fernet(key)
        token = f.encrypt(new_application_password.encode("utf-8"))
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        query = '''INSERT INTO %s (username, application, password, salt)
                VALUES (%s, %s, %s, %s);'''
        cursor.execute(query, (username,
                               new_application_username,
                               new_application_name,
                               token,
                               salt))
        conn.commit()
        return True, new_application_name, new_application_username, new_application_password
    except Error as e:
        print(e)
        return False
