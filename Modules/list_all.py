"""This module lists all records for the user
"""
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from utilities import derive_fernet_key, get_account_id

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"),
                               password=os.getenv("PASSWORD"),
                               host=os.getenv("HOST"),
                               database=os.getenv("DATABASE"),
                               charset=os.getenv("CHARSET"),
                               collation=os.getenv("COLLATION"))
cursor = conn.cursor()


def new_list_all_records(username, master_password):
    # Begin by getting the accountID
    account_id = get_account_id(username)

    try:
        search_query = '''SELECT recordID, applicationUsername, applicationName
                          FROM user_application_records
                          WHERE accountID = %s'''
        cursor.execute(search_query, (account_id,))
        application_list = cursor.fetchall()
        app_encryption_key = os.getenv("ENCRYPTION_KEY")

        if not application_list:
            return False
        
        for record in application_list:
            record_id = record[0]
            application_name = record[2]
            application_uname = record[1]
            salt_search = 'SELECT salt FROM salt_records WHERE recordID = %s'
            cursor.execute(salt_search, (record_id,))
            salt = bytes(cursor.fetchone()[0], encoding='utf-8')
            enc_key_search = '''SELECT aes_decrypt(`key`, %s) FROM encryption_keys 
                                WHERE recordID = %s'''
            cursor.execute(enc_key_search, (app_encryption_key, record_id))
            enc_key = cursor.fetchone()[0]
            app_psw_search = '''SELECT aes_decrypt(encryptedPassword, %s) FROM application_passwords
                                WHERE recordID = %s'''
            cursor.execute(app_psw_search, (enc_key, record_id))
            encrypted_password = cursor.fetchone()[0].decode('utf-8')
            fernet_key = derive_fernet_key(bytes(master_password, encoding='utf-8'), salt)
            f = Fernet(fernet_key)
            decrypted_password = f.decrypt(encrypted_password).decode('utf-8')
            print(application_name, application_uname, decrypted_password)
            
    except Error as e:
        print(f'An error has occured: {e}')
    finally:
        cursor.close()
        conn.close()
