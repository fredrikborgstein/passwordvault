""" Add a record to the database for the user

    Returns:
        Boolean: Returns True if the record was
        successfully added, False if the record already exists
"""
import os
import mysql.connector
import tkinter as tk
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from Modules.utilities import create_fernet_key, get_account_id
from Modules.password_check import password_check

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"),
                               password=os.getenv("PASSWORD"),
                               host=os.getenv("HOST"),
                               database=os.getenv("DATABASE"),
                               charset=os.getenv("CHARSET"),
                               collation=os.getenv("COLLATION"))
cursor = conn.cursor()


def add_record(master_password, username, app_username, app_password, application_name):
    # Start by fetching accountID for the useraccount
    account_id = get_account_id(username)

    # Check if the new record is already in the database

    search_query = '''SELECT applicationName FROM user_application_records
                      WHERE accountID = %s AND applicationName = %s '''
    cursor.execute(search_query, (account_id, application_name))
    does_exist = cursor.fetchone()
    print(does_exist)

    if does_exist:
        return False

    if password_check(app_password):
        tk.messagebox.showerror('Error', "This password is in a list of commonly used passwords, please choose another!")  # noqa: E501

    # If the record doesn't exist, create the record
    key, salt = create_fernet_key(bytes(master_password, encoding='utf-8'))
    fernet_key = Fernet(key)
    encryption_key = Fernet.generate_key()
    app_encryption_key = os.getenv("ENCRYPTION_KEY")
    fernet_token = fernet_key.encrypt(app_password.encode("utf-8"))
    insert_uname_appname = '''INSERT INTO user_application_records(applicationUsername,
                              applicationName, accountID) VALUES(%s, %s, %s)'''
    cursor.execute(insert_uname_appname, (app_username, application_name, account_id))
    record_id = cursor.lastrowid
    insert_app_pswd = '''INSERT INTO application_passwords(encryptedPassword, recordID)
                         VALUES(aes_encrypt(%s, %s), %s)'''
    cursor.execute(insert_app_pswd, (fernet_token, encryption_key, record_id))
    insert_pswd_salt = '''INSERT INTO salt_records(salt, recordID)
                          VALUES(%s, %s)'''
    cursor.execute(insert_pswd_salt, (salt, record_id))
    insert_enc_key = '''INSERT INTO encryption_keys(recordID, `key`)
                        VALUES(%s, aes_encrypt(%s, %s))'''
    cursor.execute(insert_enc_key, (record_id, encryption_key, app_encryption_key))
    conn.commit()
    return True
