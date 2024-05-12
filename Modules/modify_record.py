"""This module is used to modify a record in the database

Returns:
    Boolean: Returns True if the record was
                successfully modified, False if the record does not exist
"""

import os
import mysql.connector
from dotenv import load_dotenv
from Modules.utilities import get_account_id
from Modules.add_record import add_record

load_dotenv()
conn = mysql.connector.connect(user=os.getenv("USER"),
                               password=os.getenv("PASSWORD"),
                               host=os.getenv("HOST"),
                               database=os.getenv("DATABASE"),
                               charset=os.getenv("CHARSET"),
                               collation=os.getenv("COLLATION"))
cursor = conn.cursor()


def modify_record(username,
                  master_password,
                  record_to_modify,
                  new_app_name,
                  new_app_uname,
                  new_app_psw):
    # Begin by getting accountID
    account_id = get_account_id(username)

    # Check if the record exists

    exist_search = '''SELECT applicationName FROM user_application_records
                        WHERE accountID = %s'''
    cursor.execute(exist_search, (account_id,))
    does_exist = cursor.fetchone()
    if not does_exist:
        print('No record found')
        return False
    delete_current_record = '''DELETE FROM user_application_records
                                WHERE applicationName = %s AND accountID = %s'''
    cursor.execute(delete_current_record, (record_to_modify, account_id))
    add_record(master_password, username, new_app_uname, new_app_psw, new_app_name)
    return True
