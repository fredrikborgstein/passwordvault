# Importing external modules
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
import mysql.connector
import os
from dotenv import load_dotenv

# Importing internal modules
from Modules.add_record import add_record
# from Modules.retrieve_record import retrieve_record
from Modules.authentication import authenticate
from Modules.create_user import create_user
# from Modules.list_all import list_all_records
# from Modules.modify_record import modify_record
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

current_frame = "loginframe"
master_password = ""
account_username = ""

def back_to_main_menu():
    if current_frame == "addrecordframe":
        addrecordframe.place_forget()
    elif current_frame == "retrieverecordframe":
        retrieverecordframe.place_forget()
    elif current_frame == "modifyrecordframe":
        modifyrecordframe.place_forget()
    elif current_frame == "listallrecordsframe":
        listallrecordsframe.place_forget()
    mainmenuframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Creating the login window with widgets

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
    modifyrecordframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def go_to_list_all_records():
    global current_frame
    current_frame = "listallrecordsframe"
    mainmenuframe.place_forget()
    listallrecordsframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def logout():
    global current_frame
    current_frame = "loginframe"
    mainmenuframe.place_forget()
    loginframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

mainmenuframe = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15, )

l4 = customtkinter.CTkLabel(master=mainmenuframe, text="Main Menu", font=("Century Gothic", 20))
l4.place(x=110, y=45)

button5 = customtkinter.CTkButton(master=mainmenuframe, text="Add Record", width=220, font=("Century Gothic", 12), corner_radius=6, command=go_to_add_record)
button5.place(x=50, y=100)
button6 = customtkinter.CTkButton(master=mainmenuframe, text="Retrieve Record", width=220, font=("Century Gothic", 12), corner_radius=6, command=go_to_retrieve_record)
button6.place(x=50, y=145)
button7 = customtkinter.CTkButton(master=mainmenuframe, text="Modify Record", width=220, font=("Century Gothic", 12), corner_radius=6, command=go_to_modify_record)
button7.place(x=50, y=190)
button8 = customtkinter.CTkButton(master=mainmenuframe, text="List All Records", width=220, font=("Century Gothic", 12), corner_radius=6, command=go_to_list_all_records)
button8.place(x=50, y=235)
button9 = customtkinter.CTkButton(master=mainmenuframe, text="Logout", width=220, font=("Century Gothic", 12), corner_radius=6, command=logout)
button9.place(x=50, y=280)

# Creating the add record window with widgets

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


# Creating the retrieve record window with widgets

retrieverecordframe = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15, )

l6 = customtkinter.CTkLabel(master=retrieverecordframe, text="Retrieve Record", font=("Century Gothic", 20))
l6.place(x=110, y=45)

# Creating the modify record window with widgets

modifyrecordframe = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15, )

l7 = customtkinter.CTkLabel(master=modifyrecordframe, text="Modify Record", font=("Century Gothic", 20))
l7.place(x=110, y=45)

# Creating the list all records window with widgets

listallrecordsframe = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15, )

l8 = customtkinter.CTkLabel(master=listallrecordsframe, text="List All Records", font=("Century Gothic", 20))
l8.place(x=110, y=45)

# Running the application loop
app.mainloop()