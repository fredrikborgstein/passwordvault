""" This module is used to fetch all records for the user from the database

    Returns:
        list: Returns a list of all records for the user
"""
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"),
                               password=os.getenv("PASSWORD"),
                               host=os.getenv("HOST"),
                               database=os.getenv("DATABASE"),
                               charset=os.getenv("CHARSET"),
                               collation=os.getenv("COLLATION"))
cursor = conn.cursor()


def on_initiation():
    """ This module is used to fetch all records for the user from the database

    Returns:
        list: Returns a list of all records for the user
    """
    try:
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        cursor.execute('SELECT * FROM master_account_records;')
        account_records = cursor.fetchall()
        if account_records:
            return account_records
        return None
    except Error as error:
        print("Error", "An error has occured: ", error)
    finally:
        cursor.close()
        conn.close()
