""" This module retrieves a record from the database

Returns:
    Boolean: Returns True if the record was
    successfully retrieved, False if the record does not exist
"""
import os
import mysql.connector
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from Modules.utilities import derive_fernet_key, get_account_id

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"),
                               password=os.getenv("PASSWORD"),
                               host=os.getenv("HOST"),
                               database=os.getenv("DATABASE"),
                               charset=os.getenv("CHARSET"),
                               collation=os.getenv("COLLATION"))
cursor = conn.cursor()


def retrieve_record(username, master_password, search_query):
    # Retrieve accountID first
    account_id = get_account_id(username)
    app_encryption_key = os.getenv("ENCRYPTION_KEY")

    check_app = '''SELECT recordID, applicationName, applicationUsername
                   FROM user_application_records
                   WHERE applicationName = %s AND accountID = %s'''
    cursor.execute(check_app, (search_query, account_id))
    account_records = cursor.fetchone()

    if not account_records:
        print('Error')
        return False

    app_name = account_records[2]
    app_uname = account_records[1]
    record_id = account_records[0]

    search_salt = '''SELECT salt FROM salt_records
                     WHERE recordID = %s'''
    cursor.execute(search_salt, (record_id,))
    salt = bytes(cursor.fetchone()[0], encoding='utf-8')
    search_enc_key = '''SELECT aes_decrypt(`key`, %s) FROM encryption_keys
                        WHERE recordID = %s'''
    cursor.execute(search_enc_key, (app_encryption_key, record_id))
    key = cursor.fetchone()[0]
    search_psw = '''SELECT aes_decrypt(encryptedPassword, %s) FROM application_passwords
                    WHERE recordID = %s'''
    cursor.execute(search_psw, (key, record_id))
    encrypted_password = cursor.fetchone()[0].decode('utf-8')
    fernet_key = derive_fernet_key(bytes(master_password, encoding='utf-8'), salt)
    f = Fernet(fernet_key)
    decrypted_password = f.decrypt(encrypted_password).decode('utf-8')
    return True, app_uname, app_name, decrypted_password
