import mysql.connector
import os
import bcrypt
from dotenv import load_dotenv, dotenv_values

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
cursor = conn.cursor()




def authenticate():
    username = input("Enter your username: ")
    user_provided_password = input("Enter your password: ")
    encryption_key = os.getenv("ENCRYPTION_KEY")
    try:
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        cursor.execute('SELECT aes_decrypt(accountPassword, %s) FROM master_account_records WHERE accountUsername = %s', (encryption_key, username))
        account_information = cursor.fetchone()
        if account_information:
            decrypted_password = account_information[0].decode('utf-8')
            if bcrypt.checkpw(user_provided_password.encode('utf-8'), decrypted_password.encode('utf-8')):
                print("Password is correct")
            else:
                print("Password is incorrect")
        else:
            print("No record found for the provided username.")
    except Exception as error:
        print("Error", "An error has occurred:", error)
    finally:
        cursor.close()
        conn.close()

    return username, user_provided_password
