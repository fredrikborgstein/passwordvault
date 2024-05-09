import mysql.connector
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from fernet_key_generation import create_fernet_key



load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
cursor = conn.cursor()

def add_record(username, master_password):

    application = input("Enter the application: ")

    cursor.execute('SELECT application FROM {} WHERE application = "{}";'.format(username, application))
    record = cursor.fetchall()
    if not record:
        app_username = input("Enter your username for the application: ")
        password = input("Enter the password: ")
        key, salt = create_fernet_key(bytes(master_password, encoding="utf-8"))
        f = Fernet(key)
        token = f.encrypt(password.encode("utf-8"))
        print(key)
        print(salt)
        try:
            cursor.execute(f'USE {os.getenv("DATABASE")} ')
            query = 'INSERT INTO {} (username, application, password, salt) VALUES (%s, %s, %s, %s);'.format(username)
            cursor.execute(query, (app_username, application, token, salt))
            conn.commit()
        except Exception as error:
            print("Error", "An error has occured: ", error)
        finally:
            cursor.close()
            conn.close()
    else:
        print("A record for that application already exists.")
        return
    
add_record("fredrik", "test")

