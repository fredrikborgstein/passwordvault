""" Add a record to the database for the user

    Returns:
        Boolean: Returns True if the record was successfully added, False if the record already exists
"""
import os
import mysql.connector
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

def add_record(master_password, username, app_username, app_password, app):
    """Adds a record to the database for the user

    Args:
        master_password (string): the users master password for the application
        username (string): the username of the user
        app_username (string): the username for the application being added to the db record
        app_password (string): the password for the application being added to the db record
        app (string): the name of the application being added to the db record

    Returns:
        boolean: returns True if the record was successfully added, False if the record already exists
    """
    cursor.execute(f'USE {os.getenv("DATABASE")} ')
    cursor.execute('SELECT application FROM {} WHERE application = "{}";'.format(username, app))
    record = cursor.fetchall()
    if not record:
        key, salt = create_fernet_key(bytes(master_password, encoding="utf-8"))
        f = Fernet(key)
        token = f.encrypt(app_password.encode("utf-8"))

        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        query = 'INSERT INTO {} (username, application, password, salt) VALUES (%s, %s, %s, %s);'.format(username)
        cursor.execute(query, (app_username, app, token, salt))
        conn.commit()
        return True
    else:
        return False
    


