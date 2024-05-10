import mysql.connector
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from utilities import derive_fernet_key

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
cursor = conn.cursor()

def list_all_records(username, master_password):
    try:
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        cursor.execute(f'SELECT * FROM {username};')
        record = cursor.fetchall()

        for list in record:
            
           application_name = list[2]
           application_username = list[1]
           application_encrypted_password = list[3]
           application_salt = list[4]

           salt = bytes(application_salt, encoding="utf-8")
           key = derive_fernet_key(bytes(master_password, encoding="utf-8"), salt)
           f = Fernet(key)
           decrypted_password = f.decrypt(application_encrypted_password).decode("utf-8")
           print("-" * 50)
           print(f"Application: {application_name}")
           print(f"Username: {application_username}")
           print(f"Password: {decrypted_password}")
           
    except Exception as error:
        print("Error", "An error has occured: ", error)
    finally:
        cursor.close()
        conn.close()
