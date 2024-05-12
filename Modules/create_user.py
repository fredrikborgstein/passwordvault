"""Module to create a user in the database

Returns:
     Boolean: returns True if the user was successfully created, False if the user already exists
"""
import os
import mysql.connector
import bcrypt
from dotenv import load_dotenv

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"),
                               password=os.getenv("PASSWORD"),
                               host=os.getenv("HOST"),
                               database=os.getenv("DATABASE"),
                               charset=os.getenv("CHARSET"),
                               collation=os.getenv("COLLATION"))
cursor = conn.cursor()


def hash_password(pass_string):
    """Hashes the password

    Args:
        pass_string (string): the password to be hashed

    Returns:
        string: the hashed password
    """
    hashed_password = bcrypt.hashpw(pass_string.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def new_create_user_func(username, password):
    hashed_password = hash_password(password)
    bcrypt_hash_utf8 = hashed_password.decode('utf-8')
    encryption_key = os.getenv("ENCRYPTION_KEY")

    # Check to see if username already exists in DB

    user_query = '''SELECT accountUsername FROM master_accounts
                    WHERE accountUsername = %s'''
    cursor.execute(user_query, (username,))
    user_ex = cursor.fetchone()
    print(user_ex)
    if user_ex:
        return False

    # Create the user in the master_accounts
    create_the_user = '''INSERT INTO master_accounts(accountUsername)
                         VALUES(%s)'''
    cursor.execute(create_the_user, (username,))
    account_id = cursor.lastrowid
    print(account_id)
    # Add the password to the hashed_passwords
    add_password = '''INSERT INTO password_hashes(hashedPassword, accountID)
                      VALUES(aes_encrypt(%s, %s), %s)'''
    cursor.execute(add_password, (bcrypt_hash_utf8, encryption_key, account_id))
    conn.commit()
    return True


new_create_user_func('fredrik', 'test')


def create_user(username, password):
    """Creates a user in the database

    Args:
        username (string): The username of the user
        password (string): The password of the user

    Returns:
        Boolean: returns True if the user was successfully created, False if the user already exists
    """
    hashed_password = hash_password(password)
    bcrypt_hash_utf8 = hashed_password.decode('utf-8')
    encryption_key = os.getenv("ENCRYPTION_KEY")

    # Check to see if the user already exists
    cursor.execute(f'''SELECT accountUsername FROM master_account_records
                        WHERE accountUsername = "{username}"''')
    if cursor.fetchone():
        return False
    else:
        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        cursor.execute('''INSERT INTO master_account_records (accountUsername, accountPassword)
                        VALUES (%s, aes_encrypt(%s, %s))''',
                       (username, bcrypt_hash_utf8, encryption_key))
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {username}
                       (id INT AUTO_INCREMENT PRIMARY KEY,
                       username VARCHAR(255) NOT NULL,
                       application VARCHAR(255) NOT NULL,
                       password BLOB(255) NOT NULL,
                       salt BLOB(255) NOT NULL)''')
        conn.commit()
        return True
