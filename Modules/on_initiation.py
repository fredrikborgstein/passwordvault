import mysql.connector
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
cursor = conn.cursor()

def on_initiation():
    try:
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        cursor.execute('SELECT * FROM master_account_records;')
        account_records = cursor.fetchall()
        return account_records
    except Exception as error:
        print("Error", "An error has occured: ", error)
    finally:
        cursor.close()
        conn.close()
