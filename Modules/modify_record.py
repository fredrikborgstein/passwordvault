import mysql.connector
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from utilities import derive_fernet_key, create_fernet_key

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
cursor = conn.cursor()

def modify_record(username, master_password):
    record_to_modify = input("Enter the application name to modify: ")

    try:
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        cursor.execute(f'SELECT * FROM {username} WHERE application = "{record_to_modify}";')
        record = cursor.fetchall()
        application_name = record[0][2]
        application_username = record[0][1]
        cursor.execute(f'SELECT password FROM {username} WHERE application = "{record_to_modify}";')
        application_encrypted_password = cursor.fetchone()[0]
        cursor.execute(f'SELECT salt FROM {username} WHERE application = "{record_to_modify}";')
        application_salt = cursor.fetchone()[0]
        salt = bytes(application_salt, encoding="utf-8")
        key = derive_fernet_key(bytes(master_password, encoding="utf-8"), salt)
        f = Fernet(key)
        application_password = f.decrypt(application_encrypted_password).decode("utf-8")

        print("These are the current details we have for this application:")
        print(f"Application: {application_name}")
        print(f"Username: {application_username}")
        print(f"Password: {application_password}")
        print("-" * 50)
        print("Please enter the new details for this application")
        new_application_name = input("Enter the application name: ")
        new_application_username = input("Enter the application username: ")
        new_application_password = input("Enter the application password: ")

        if new_application_name == application_name and new_application_username == application_username and new_application_password == application_password:
            print("No changes made")
        else:
            cursor.execute(f'DELETE FROM {username} WHERE application = "{record_to_modify}";')
        
            key, salt = create_fernet_key(bytes(master_password, encoding="utf-8"))
            f = Fernet(key)
            token = f.encrypt(new_application_password.encode("utf-8"))
            cursor.execute(f'USE {os.getenv("DATABASE")} ')
            query = 'INSERT INTO {} (username, application, password, salt) VALUES (%s, %s, %s, %s);'.format(username)
            cursor.execute(query, (new_application_username, new_application_name, token, salt))
            conn.commit()

            print("Record updated successfully")
            print("These are the new details for this application:")
            print(f"Application: {new_application_name}")
            print(f"Username: {new_application_username}")
            print(f"Password: {new_application_password}")
            print("-" * 50)
        
    except Exception as error:
        print("Error", "An error has occured: ", error)
    finally:
        cursor.close()
        conn.close()

