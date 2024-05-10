import mysql.connector
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from Modules.utilities import create_fernet_key

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
cursor = conn.cursor()

def add_record(master_password, username, app_username, app_password, app):
    cursor.execute(f'USE {os.getenv("DATABASE")} ')
    cursor.execute('SELECT application FROM {} WHERE application = "{}";'.format(username, app))
    record = cursor.fetchall()
    if not record:
        key, salt = create_fernet_key(bytes(master_password, encoding="utf-8"))
        f = Fernet(key)
        token = f.encrypt(app_password.encode("utf-8"))

        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        query = 'INSERT INTO {} (username, application, password, salt) VALUES (%s, %s, %s, %s);'.format(username)
        cursor.execute(query, (app_username, app, token, salt))
        conn.commit()
        return True
    else:
        return False
    


