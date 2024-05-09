import mysql.connector
import os
import hashlib
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv, dotenv_values

load_dotenv()
conn = mysql.connector.connect(user = os.getenv("USER"), password = os.getenv("PASSWORD"), host = os.getenv("HOST"), database = os.getenv("DATABASE"), charset = os.getenv("CHARSET"), collation = os.getenv("COLLATION"))
cursor = conn.cursor()

def hash_password(pass_string):
    return hashlib.sha512(pass_string.encode("utf-8")).hexdigest()

# Connect to the DB to check whether any DB records exists in master accounts
def check_if_db_empty():
    try:
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        cursor.execute('SELECT * FROM master_account_records;')
        account_records = cursor.fetchall()
        print(account_records)

    except Exception as error:
        print("Error", "An error has occured: ", error)

    return account_records

# If there is no records, prompt user to create a master account
def create_first_user():
    print("No records found")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)
    encryption_key = hashed_password[0:32]

    try:
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        cursor.execute(f'INSERT INTO master_account_records (accountUsername, accountPassword) VALUES ("{username}", aes_encrypt("{hashed_password}", "{encryption_key}"));')
        conn.commit()
    except Exception as error:
        print("Error", "An error has occured: ", error)
        
        
# Else, prompt for password and username
def user_login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)
    encryption_key = hashed_password[0:32]

    try:
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        cursor.execute(f'SELECT * FROM master_account_records WHERE accountUsername = "{username}";')
        account_record = cursor.fetchall()
        cursor.execute(f'SELECT aes_decrypt(accountPassword, "{encryption_key}") FROM master_account_records WHERE accountUsername = "{username}";')
        decrypted_password = cursor.fetchall()
        print(decrypted_password)
        print(account_record)
        
    except Exception as error:
        print("Error", "An error has occured: ", error)
        

    if account_record:
        if decrypted_password == hashed_password:
            print("Success")
        else:
            print("Incorrect password")
    else:
        print("No such username exists")

def test():
    if check_if_db_empty():
        user_login()
    else:
        create_first_user()

# If username and password is correct, take user to main application

try:
    test()
    cursor.close()
    conn.close()
except Exception as error:
    print("An error has occured", error)
    cursor.close()
    conn.close()