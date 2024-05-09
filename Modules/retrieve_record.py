import mysql.connector
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from fernet_key_generation import derive_fernet_key

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
cursor = conn.cursor()



def retrieve_record(username, master_password):
    search_query = input("Enter the application you want to retrieve: ")
    try:
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        cursor.execute(f'SELECT * FROM {username} WHERE application = "{search_query}";')
        record = cursor.fetchall()

        if not record:
            print("No record found for that application.")
        else:
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

            print(f"Application: {application}")
            print(f"Username: {app_username}")
            print(f"Password: {decrypted_password}")

        
    except Exception as error:
        print("Error", "An error has occured: ", error)
    finally:
        cursor.close()
        conn.close()


