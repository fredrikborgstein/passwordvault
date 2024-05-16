""" This module is run when the application is opened, to check wether the
    application has been run before
    and if not, it creates the initial information such as encryption key.

    Returns:
        list: Returns a list of all records for the user
"""
import os
import mysql.connector
import tkinter as tk
from mysql.connector import Error
from dotenv import load_dotenv
from Modules.utilities import set_encryption_key

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"),
                               password=os.getenv("PASSWORD"),
                               host=os.getenv("HOST"),
                               database=os.getenv("DATABASE"),
                               charset=os.getenv("CHARSET"),
                               collation=os.getenv("COLLATION"))
cursor = conn.cursor()


def check_if_first_time_use():
    try:
        cursor.execute('SELECT * FROM master_accounts')
        account_records = cursor.fetchall()

        if account_records:
            return False
    except Error as e:
        tk.messagebox.showerror('Error',
                                f'There was an error connecting to the Database {e}')

    set_encryption_key()
    return True
