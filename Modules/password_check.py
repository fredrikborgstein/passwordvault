""" Functions used to check if the user's password is in the list of common passwords
"""
import os


def load_common_passwords(file_path):
    """ Loads the .txt file of common passwords into a set

    Args:
        file_path (str): the string indicating where the file is located

    Returns:
        set: returns a set with the passwords in
    """
    with open(file_path, 'r') as file:
        common_passwords = {line.strip() for line in file}
    return common_passwords


def is_common_password(password, common_passwords):
    """ Checks whether the users password is in a set of common passwords

    Args:
        password (str): The users password
        common_passwords (set): The set with common passwords

    Returns:
        Boolean: Returns a True if the password is in the list, False if not.
    """
    return password in common_passwords


def password_check(password):
    """ Loads the .txt file, creates the set, checks if the password is in the list or not

    Args:
        password (str): The string of the user's password

    Returns:
        Boolean: Returns True if the password is found in the list, False if not.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    common_passwords_file = os.path.join(script_dir, '../Assets/common_passwords.txt')
    common_passwords = load_common_passwords(common_passwords_file)

    if is_common_password(password, common_passwords):
        return True
    else:
        return False
