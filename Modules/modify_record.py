import mysql.connector
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from Modules.utilities import derive_fernet_key, create_fernet_key

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
cursor = conn.cursor()

def modify_record(username, master_password, record_to_modify, new_application_name, new_application_username, new_application_password):

    try:
        cursor.execute(f'DELETE FROM {username} WHERE application = "{record_to_modify}";')
        
        key, salt = create_fernet_key(bytes(master_password, encoding="utf-8"))
        f = Fernet(key)
        token = f.encrypt(new_application_password.encode("utf-8"))
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        query = 'INSERT INTO {} (username, application, password, salt) VALUES (%s, %s, %s, %s);'.format(username)
        cursor.execute(query, (new_application_username, new_application_name, token, salt))
        conn.commit()
        return True, new_application_name, new_application_username, new_application_password
    except Exception as e:
        print(e)
        return False