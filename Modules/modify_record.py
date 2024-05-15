"""This module is used to modify a record in the database

Returns:
    Boolean: Returns True if the record was
                successfully modified, False if the record does not exist
"""

import os
import mysql.connector
import tkinter as tk
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from Modules.utilities import get_account_id, create_fernet_key
from Modules.password_check import password_check


load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"),
                               password=os.getenv("PASSWORD"),
                               host=os.getenv("HOST"),
                               database=os.getenv("DATABASE"),
                               charset=os.getenv("CHARSET"),
                               collation=os.getenv("COLLATION"))
cursor = conn.cursor(buffered=True)


def modify_record(username,
                  master_password,
                  record_to_modify,
                  new_app_name,
                  new_app_uname,
                  new_app_psw):
    # Begin by getting accountID
    account_id = get_account_id(username)
    print(record_to_modify)

    # Check if the record exists

    exist_search = '''SELECT applicationName FROM user_application_records
                        WHERE accountID = %s'''
    cursor.execute(exist_search, (account_id,))
    does_exist = cursor.fetchone()
    if not does_exist:
        print('No record found')
        return False
    print(f'TEST {record_to_modify}')
    delete_current_record = '''DELETE FROM user_application_records
                                WHERE applicationName = %s AND accountID = %s'''
    cursor.execute(delete_current_record, (record_to_modify, account_id))
    if cursor.rowcount == 0:
        print(f"No record with application name '{record_to_modify}' found for user '{username}'.")
        return False

    if password_check(new_app_psw):
        tk.messagebox.showerror('Error', 'This password is in a list of commonly used passwords, please choose another!')  # noqa: E501
        return False

    key, salt = create_fernet_key(bytes(master_password, encoding='utf-8'))
    fernet_key = Fernet(key)
    encryption_key = Fernet.generate_key()
    app_encryption_key = os.getenv("ENCRYPTION_KEY")
    fernet_token = fernet_key.encrypt(new_app_psw.encode("utf-8"))
    insert_uname_appname = '''INSERT INTO user_application_records(applicationUsername,
                              applicationName, accountID) VALUES(%s, %s, %s)'''
    cursor.execute(insert_uname_appname, (new_app_uname, new_app_name, account_id))
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
