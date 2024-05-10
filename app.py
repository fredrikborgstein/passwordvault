# Importing external modules
import customtkinter
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import os
from dotenv import load_dotenv
import pyperclip
from cryptography.fernet import Fernet

# Importing internal modules
from Modules.add_record import add_record
from Modules.retrieve_record import retrieve_record
from Modules.authentication import authenticate
from Modules.create_user import create_user
from Modules.utilities import derive_fernet_key
from Modules.modify_record import modify_record
from Modules.utilities import create_fernet_key

# Creating the main window with settings and appearence

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("600x440")
app.title("VikingCrypt Protector - Login")
app.attributes('-alpha', 0.98)
app.resizable(False, False)

img1 = Image.open("Assets/background_image.jpeg")
img1 = ImageTk.PhotoImage(img1.resize((600, 440)))

l1 = customtkinter.CTkLabel(master=app, image=img1)
l1.pack()

# Global variables
current_frame = "loginframe"
master_password = ""
account_username = ""

#TODO:
# Add about window/page
# Add help window/page
# Add text at bottow of main window with version number

# Functions

def back_to_main_menu():
    global current_frame
    if current_frame == "addrecordframe":
        addrecordframe.place_forget()
    elif current_frame == "retrieverecordframe":
        retrieverecordframe.place_forget()
    elif current_frame == "modifyrecordframe":
        modifyrecordframe.place_forget()
    elif current_frame == "listallrecordsframe":
        listallrecordsframe.place_forget()
    elif current_frame == "generatepasswordframe":
        generatepasswordframe.place_forget()
    mainmenuframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    current_frame = "mainmenuframe"

def login():
    username = entry1.get()
    password = entry2.get()
    is_user_authenticated = False

    try:
        load_dotenv()
        conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
        cursor = conn.cursor()
        is_user_authenticated = authenticate(username, password)
        if not is_user_authenticated:
            tk.messagebox.showerror("Error", "The username or password is incorrect.")
    except Exception as error:
        tk.messagebox.showerror("Error", f"An error has occured: {error}")
    finally:
        cursor.close()
        conn.close()
    
    loginframe.place_forget()
    mainmenuframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    global master_password, account_username
    master_password = password
    account_username = username
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    entry1.focus()
    
def change_to_register():
    loginframe.place_forget()
    registerframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def generate_password():
    if current_frame == "generatepasswordframe":
        length = entry12.get()
    else:
        length = "16"
    password = ""
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+"
    for i in range(int(length)):
        password += characters[ord(os.urandom(1)) % len(characters)]
    generated_password.configure(text=password)
    button22.place(x=50, y=250)

    if current_frame == "addrecordframe":
        entry7.delete(0, tk.END)
        entry7.insert(0, password)

def back_to_login():
    registerframe.place_forget()
    loginframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def register():
    username = entry3.get()
    password = entry4.get()
    is_user_created = False

    try:
        load_dotenv()
        conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
        cursor = conn.cursor()
        is_user_created = create_user(username, password)
        if not is_user_created:
            tk.messagebox.showerror("Error", "The username is already taken.")  

    except Exception as error:
        tk.messagebox.showerror("Error", f"An error has occured: {error}")
    finally:
        cursor.close()
        conn.close()
    
    registerframe.place_forget()
    mainmenuframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    global master_password, account_username
    master_password = password
    account_username = username

def go_to_add_record():
    global current_frame
    current_frame = "addrecordframe"
    mainmenuframe.place_forget()
    addrecordframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
def go_to_retrieve_record():
    global current_frame
    current_frame = "retrieverecordframe"
    mainmenuframe.place_forget()
    retrieverecordframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def go_to_modify_record():
    global current_frame
    current_frame = "modifyrecordframe"
    mainmenuframe.place_forget()
    retrieverecordframe.place_forget()
    modifyrecordframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def go_to_list_all_records():
    global current_frame
    current_frame = "listallrecordsframe"
    mainmenuframe.place_forget()
    listallrecordsframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    on_open_listall()

def logout():
    global current_frame
    current_frame = "loginframe"
    mainmenuframe.place_forget()
    loginframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def go_to_generate_password():
    global current_frame
    current_frame = "generatepasswordframe"
    mainmenuframe.place_forget()
    generatepasswordframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def create_record():
    username = entry5.get()
    application = entry6.get()
    password = entry7.get()

    try:
        load_dotenv()
        conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
        cursor = conn.cursor()
        is_record_created = add_record(master_password, account_username, username, password, application)
        if not is_record_created:
            tk.messagebox.showerror("Error", "A record for that application already exists.")
        else:
            tk.messagebox.showinfo("Success", "The record has been created successfully.")
            entry5.delete(0, tk.END)
            entry6.delete(0, tk.END)
            entry7.delete(0, tk.END)
            entry5.focus()
    except Exception as error:
        tk.messagebox.showerror("Error", f"An error has occured: {error}")
    finally:
        cursor.close()
        conn.close()

def search_record():
    application = entry8.get()

    try:
        load_dotenv()
        conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
        cursor = conn.cursor()
        is_record_retrieved, app_username, app, app_dec_password = retrieve_record(account_username, master_password, application)
        if not is_record_retrieved:
            tk.messagebox.showerror("Error", "No record found for that application.")
        else:
            entry8.delete(0, tk.END)
            entry8.focus()
            label_app.configure(text="Application: ")
            label_username.configure(text="Username: ")
            label_password.configure(text="Password: ")
            label_app_result.configure(text=app)
            label_username_result.configure(text=app_username)
            label_password_result.configure(text=app_dec_password)
            button14.place(x=40, y=260)
            button15.place(x=160, y=260)

    except:
        tk.messagebox.showerror("Error", "An error has occured. Please try again later.")
    finally:
        cursor.close()
        conn.close()

def copy_password():
    if current_frame == "retrieverecordframe":
        pyperclip.copy(label_password_result.cget("text"))
    elif current_frame == "generatepasswordframe":
        pyperclip.copy(generated_password.cget("text"))
    tk.messagebox.showinfo("Success", "The password has been copied to the clipboard.")
    button14.place_forget()

def modify_searched_record():
    application = entry8.get()
    new_app_name = entry9.get()
    new_app_username = entry10.get()
    new_app_password = entry11.get()

    try:
        load_dotenv()
        conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
        cursor = conn.cursor()
        is_record_modified, app_username, app, app_dec_password = modify_record(account_username, master_password, application, new_app_name, new_app_username, new_app_password)
        if not is_record_modified:
            tk.messagebox.showerror("Error", "No changes made to the record")
        else:
            tk.messagebox.showinfo("Success", "The record has been modified successfully.")
            entry9.delete(0, tk.END)
            entry10.delete(0, tk.END)
            entry11.delete(0, tk.END)

            label_app_mod.configure(text="Application: ")
            label_app_result_mod.configure(text=app)
            label_username_mod.configure(text="Username: ")
            label_username_result_mod.configure(text=app_username)
            label_password_mod.configure(text="Password: ")
            label_password_result_mod.configure(text=app_dec_password)
            button16.place_forget()
    
    except Exception as error:
        tk.messagebox.showerror("Error", f"An error has occured: {error}")
    finally:
        cursor.close()
        conn.close()
        back_to_main_menu()

def on_open_listall():

    style = ttk.Style()
    style.configure("Treeview", background="black", fieldbackground="black", foreground="white", font=("Century Gothic", 12), rowheight=25)
    style.configure("Treeview.Heading", font=("Century Gothic", 12), background="black")
    style.configure("Treeview.Item", font=("Century Gothic", 12), background="black")


    tree=ttk.Treeview(master=listallrecordsframe, columns=("Application", "Username", "Password"), show="headings", height=10)
    tree.heading("Application", text="Application")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")
    tree.column("Application", width=100)
    tree.column("Username", width=100)
    tree.column("Password", width=100)
    tree.place(x=50, y=70, width=400, height=260)

    try:
        load_dotenv()
        conn = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PASSWORD"), host=os.getenv("HOST"), database=os.getenv("DATABASE"), charset=os.getenv("CHARSET"), collation=os.getenv("COLLATION"))
        cursor = conn.cursor()

        cursor.execute(f'USE {os.getenv("DATABASE")} ')
        cursor.execute(f'SELECT * FROM {account_username};')
        record = cursor.fetchall()

        for list in record:
                
            application_name = list[2]
            application_username = list[1]
            application_encrypted_password = list[3]
            application_salt = list[4]

            salt = bytes(application_salt, encoding="utf-8")
            key = derive_fernet_key(bytes(master_password, encoding="utf-8"), salt)
            f = Fernet(key)
            decrypted_password = f.decrypt(application_encrypted_password).decode("utf-8")
            tree.insert("", "end", values=(application_name, application_username, decrypted_password))
            

    except:
        tk.messagebox.showerror("Error", "An error has occured. Please try again later.")
    finally:
        cursor.close()
        conn.close()
    
def back_to_main_menu_tree():
    listallrecordsframe.place_forget()
    mainmenuframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    for col in tree['columns']:
        tree.heading(col, text="")
    tree.delete(*tree.get_children())
    tree["columns"] = ()


# Creating the login window with widgets

loginframe = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15, )
loginframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

l2 = customtkinter.CTkLabel(master=loginframe, text="Log into your account", font=("Century Gothic", 20))
l2.place(x=50, y=45)

entry1 = customtkinter.CTkEntry(master=loginframe, width=220, placeholder_text="Username", font=("Century Gothic", 12))
entry1.place(x=50, y=110)

entry2 = customtkinter.CTkEntry(master=loginframe, width=220, placeholder_text="Password", font=("Century Gothic", 12))
entry2.configure(show="*")
entry2.place(x=50, y=165)

button1 = customtkinter.CTkButton(master=loginframe, text="Login", width=100, font=("Century Gothic", 12), corner_radius=6, command=login)
button1.place(x=50, y=240)
button2 = customtkinter.CTkButton(master=loginframe, text="Create Account", width=100, font=("Century Gothic", 12), corner_radius=6, command=change_to_register)
button2.place(x=160, y=240)

# Creating the register user window with widgets

registerframe = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15, )

l3 = customtkinter.CTkLabel(master=registerframe, text="Create an account", font=("Century Gothic", 20))
l3.place(x=50, y=45)

entry3 = customtkinter.CTkEntry(master=registerframe, width=220, placeholder_text="Username", font=("Century Gothic", 12))
entry3.place(x=50, y=110)
entry4 = customtkinter.CTkEntry(master=registerframe, width=220, placeholder_text="Password", font=("Century Gothic", 12))
entry4.configure(show="*")
entry4.place(x=50, y=165)

button3 = customtkinter.CTkButton(master=registerframe, text="Register", width=100, font=("Century Gothic", 12), corner_radius=6, command=register)
button3.place(x=50, y=240)
button4 = customtkinter.CTkButton(master=registerframe, text="Back to login", width=100, font=("Century Gothic", 12), corner_radius=6, command=back_to_login)
button4.place(x=160, y=240)

# Creating the main menu window with widgets

mainmenuframe = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15, )

l4 = customtkinter.CTkLabel(master=mainmenuframe, text="Main Menu", font=("Century Gothic", 20))
l4.place(x=110, y=45)

button5 = customtkinter.CTkButton(master=mainmenuframe, text="Add Record", width=220, font=("Century Gothic", 12), corner_radius=6, command=go_to_add_record)
button5.place(x=50, y=100)
button6 = customtkinter.CTkButton(master=mainmenuframe, text="Retrieve Record", width=220, font=("Century Gothic", 12), corner_radius=6, command=go_to_retrieve_record)
button6.place(x=50, y=145)
button8 = customtkinter.CTkButton(master=mainmenuframe, text="List All Records", width=220, font=("Century Gothic", 12), corner_radius=6, command=go_to_list_all_records)
button8.place(x=50, y=235)
button9 = customtkinter.CTkButton(master=mainmenuframe, text="Logout", width=220, font=("Century Gothic", 12), corner_radius=6, command=logout)
button9.place(x=50, y=280)
button19 = customtkinter.CTkButton(master=mainmenuframe, text="Generate Password", width=220, font=("Century Gothic", 12), corner_radius=6, command=go_to_generate_password)
button19.place(x=50, y=190)

# Creating the add record window with widgets

addrecordframe = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15, )

l5 = customtkinter.CTkLabel(master=addrecordframe, text="Add Record", font=("Century Gothic", 20))
l5.place(x=110, y=45)

entry5 = customtkinter.CTkEntry(master=addrecordframe, width=220, placeholder_text="Username", font=("Century Gothic", 12))
entry5.place(x=50, y=100)
entry6 = customtkinter.CTkEntry(master=addrecordframe, width=220, placeholder_text="Application", font=("Century Gothic", 12))
entry6.place(x=50, y=145)
entry7 = customtkinter.CTkEntry(master=addrecordframe, width=220, placeholder_text="Password", font=("Century Gothic", 12))
entry7.place(x=50, y=190)

button10 = customtkinter.CTkButton(master=addrecordframe, text="Add Record", width=100, font=("Century Gothic", 12), corner_radius=6, command=create_record)
button10.place(x=50, y=240)
button11 = customtkinter.CTkButton(master=addrecordframe, text="Back to Main Menu", width=100, font=("Century Gothic", 12), corner_radius=6, command=back_to_main_menu)
button11.place(x=160, y=240)
button23 = customtkinter.CTkButton(master=addrecordframe, text="Generate Password", width=100, font=("Century Gothic", 12), corner_radius=6, command=generate_password)
button23.place(x=50, y=280)


# Creating the retrieve record window with widgets

retrieverecordframe = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15, )

l6 = customtkinter.CTkLabel(master=retrieverecordframe, text="Retrieve Record", font=("Century Gothic", 20))
l6.place(x=90, y=45)

entry8 = customtkinter.CTkEntry(master=retrieverecordframe, width=220, placeholder_text="Application", font=("Century Gothic", 12))
entry8.place(x=50, y=100)

button12 = customtkinter.CTkButton(master=retrieverecordframe, text="Search", width=100, font=("Century Gothic", 12), corner_radius=6, command=search_record)
button12.place(x=40, y=145)
button13 = customtkinter.CTkButton(master=retrieverecordframe, text="Main Menu", width=100, font=("Century Gothic", 12), corner_radius=6, command=back_to_main_menu)
button13.place(x=160, y=145)

label_app = customtkinter.CTkLabel(master=retrieverecordframe, text="", font=("Century Gothic", 12))
label_app.place(x=20, y=190)
label_app_result = customtkinter.CTkLabel(master=retrieverecordframe, text="", font=("Century Gothic", 12))
label_app_result.place(x=20, y=210)
label_username = customtkinter.CTkLabel(master=retrieverecordframe, text="", font=("Century Gothic", 12))
label_username.place(x=130, y=190)
label_username_result = customtkinter.CTkLabel(master=retrieverecordframe, text="", font=("Century Gothic", 12))
label_username_result.place(x=130, y=210)
label_password = customtkinter.CTkLabel(master=retrieverecordframe, text="", font=("Century Gothic", 12))
label_password.place(x=230, y=190)
label_password_result = customtkinter.CTkLabel(master=retrieverecordframe, text="", font=("Century Gothic", 12))
label_password_result.place(x=230, y=210)

button14 = customtkinter.CTkButton(master=retrieverecordframe, text="Copy Password", width=100, font=("Century Gothic", 12), corner_radius=6, command=copy_password)
button15 = customtkinter.CTkButton(master=retrieverecordframe, text="Modify Record", width=100, font=("Century Gothic", 12), corner_radius=6, command=go_to_modify_record)

# Creating the modify record window with widgets
modifyrecordframe = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15, )

l7 = customtkinter.CTkLabel(master=modifyrecordframe, text="Modify Record", font=("Century Gothic", 20))
l7.place(x=90, y=45)

entry9 = customtkinter.CTkEntry(master=modifyrecordframe, width=220, placeholder_text="Application", font=("Century Gothic", 12))
entry9.place(x=50, y=100)
entry10 = customtkinter.CTkEntry(master=modifyrecordframe, width=220, placeholder_text="New Username", font=("Century Gothic", 12))
entry10.place(x=50, y=145)
entry11 = customtkinter.CTkEntry(master=modifyrecordframe, width=220, placeholder_text="New Password", font=("Century Gothic", 12))
entry11.place(x=50, y=190)

button16 = customtkinter.CTkButton(master=modifyrecordframe, text="Submit", width=100, font=("Century Gothic", 12), corner_radius=6, command=modify_searched_record)
button16.place(x=40, y=240)
button17 = customtkinter.CTkButton(master=modifyrecordframe, text="Main Menu", width=100, font=("Century Gothic", 12), corner_radius=6, command=back_to_main_menu)
button17.place(x=160, y=240)

label_app_mod = customtkinter.CTkLabel(master=retrieverecordframe, text="", font=("Century Gothic", 12))
label_app_mod.place(x=20, y=190)
label_app_result_mod = customtkinter.CTkLabel(master=retrieverecordframe, text="", font=("Century Gothic", 12))
label_app_result_mod.place(x=20, y=210)
label_username_mod = customtkinter.CTkLabel(master=retrieverecordframe, text="", font=("Century Gothic", 12))
label_username_mod.place(x=130, y=190)
label_username_result_mod = customtkinter.CTkLabel(master=retrieverecordframe, text="", font=("Century Gothic", 12))
label_username_result_mod.place(x=130, y=210)
label_password_mod = customtkinter.CTkLabel(master=retrieverecordframe, text="", font=("Century Gothic", 12))
label_password_mod.place(x=230, y=190)
label_password_result_mod = customtkinter.CTkLabel(master=retrieverecordframe, text="", font=("Century Gothic", 12))
label_password_result_mod.place(x=230, y=210)

# Creating the list all records window with widgets

listallrecordsframe = customtkinter.CTkFrame(master=l1, width=500, height=400, corner_radius=15, )

l8 = customtkinter.CTkLabel(master=listallrecordsframe, text="List All Records", font=("Century Gothic", 20))
l8.place(x=110, y=30)

tree=ttk.Treeview(master=listallrecordsframe, columns=("Application", "Username", "Password"), show="headings", height=10)

button18 = customtkinter.CTkButton(master=listallrecordsframe, text="Main Menu", width=100, font=("Century Gothic", 12), corner_radius=6, command=back_to_main_menu_tree)
button18.place(x=160, y=360)


# Creating the generate password window with widgets

generatepasswordframe = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15, )

l9 = customtkinter.CTkLabel(master=generatepasswordframe, text="Generate Password", font=("Century Gothic", 20))
l9.place(x=70, y=45)

entry12 = customtkinter.CTkEntry(master=generatepasswordframe, width=220, placeholder_text="Length", font=("Century Gothic", 12))
entry12.place(x=50, y=100)

button20 = customtkinter.CTkButton(master=generatepasswordframe, text="Generate", width=100, font=("Century Gothic", 12), corner_radius=6, command=generate_password)
button20.place(x=50, y=150)
button21 = customtkinter.CTkButton(master=generatepasswordframe, text="Main Menu", width=100, font=("Century Gothic", 12), corner_radius=6, command=back_to_main_menu)
button21.place(x=160, y=150)
button22 = customtkinter.CTkButton(master=generatepasswordframe, text="Copy Password", width=100, font=("Century Gothic", 12), corner_radius=6, command=copy_password)

generated_password = customtkinter.CTkLabel(master=generatepasswordframe, text="", font=("Century Gothic", 12))
generated_password.place(x=50, y=200)

# Running the application loop
app.mainloop()