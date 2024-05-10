import customtkinter
import tkinter as tk
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("600x440")
app.title("Login")

img1 = ImageTk.PhotoImage(Image.open("Assets/background_image.jpeg"))
l1 = customtkinter.CTkLabel(master=app, image=img1)
l1.pack()

frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


l2 = customtkinter.CTkLabel(master=frame, text="Log into your account", font=("Century Gothic", 20))
l2.place(x=50, y=45)

entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Username", font=("Century Gothic", 12))
entry1.place(x=50, y=110)

entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Password", font=("Century Gothic", 12))
entry2.configure(show="*")
entry2.place(x=50, y=165)

button1 = customtkinter.CTkButton(master=frame, text="Login", width=100, font=("Century Gothic", 12), corner_radius=6)
button1.place(x=50, y=240)
button2 = customtkinter.CTkButton(master=frame, text="Create Account", width=100, font=("Century Gothic", 12), corner_radius=6)
button2.place(x=160, y=240)


app.mainloop()