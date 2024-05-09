import mysql.connector
import os
import bcrypt
from dotenv import load_dotenv, dotenv_values

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
cursor = conn.cursor()

def hash_password(pass_string):
    hashed_password = bcrypt.hashpw(pass_string.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def create_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)
    bcrypt_hash_utf8 = hashed_password.decode('utf-8')
    encryption_key = os.getenv("ENCRYPTION_KEY")

    try:
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        cursor.execute('INSERT INTO master_account_records (accountUsername, accountPassword) VALUES (%s, aes_encrypt(%s, %s))', (username, bcrypt_hash_utf8, encryption_key))
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {username}(id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL, application VARCHAR(255) NOT NULL, password BLOB(255) NOT NULL, salt BLOB(255) NOT NULL)')
        conn.commit()
        
    except Exception as error:
        print("Error", "An error has occurred:", error)
    finally:
        cursor.close()
        conn.close()
    print("User created successfully")
    return username, password

