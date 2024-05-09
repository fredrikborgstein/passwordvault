from Modules.on_initiation import on_initiation
from Modules.add_record import add_record
from Modules.authentication import authenticate
from Modules.create_user import create_user
from Modules.list_all import list_all_records
from Modules.retrieve_record import retrieve_record
from Modules.modify_record import modify_record


def main():
    account_records = on_initiation()
    
    if account_records:
        print("Records found")
        username, master_password = authenticate()
    else:
        print("No records found, please create a user")
        username, master_password = create_user()
    
    print("Welcome to the password manager")
    print("Please add a password to keep stored")
    add_record(username, master_password)
    list_all_records(username, master_password)
    retrieve_record(username, master_password)
    modify_record(username, master_password)



main()

