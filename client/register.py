import customtkinter as ctk
from tkinter import messagebox

from modules.auth import register_user
from modules.validators import validate_registration

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Register")
app.geometry("500x600")
app.resizable(False, False)


def register():

    full_name = full_name_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    confirm = confirm_entry.get()

    valid, msg = validate_registration(
        full_name,
        username,
        password,
        confirm
    )

    if not valid:
        messagebox.showerror("Error", msg)
        return

    success, msg = register_user(
        full_name,
        username,
        password
    )

    if success:
        messagebox.showinfo("Success", msg)
        app.destroy()

    else:
        messagebox.showerror("Error", msg)


title = ctk.CTkLabel(
    app,
    text="Create Account",
    font=("Segoe UI", 28, "bold")
)
title.pack(pady=30)

full_name_entry = ctk.CTkEntry(
    app,
    width=320,
    placeholder_text="Full Name"
)
full_name_entry.pack(pady=10)

username_entry = ctk.CTkEntry(
    app,
    width=320,
    placeholder_text="Username"
)
username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(
    app,
    width=320,
    placeholder_text="Password",
    show="*"
)
password_entry.pack(pady=10)

confirm_entry = ctk.CTkEntry(
    app,
    width=320,
    placeholder_text="Confirm Password",
    show="*"
)
confirm_entry.pack(pady=10)

register_btn = ctk.CTkButton(
    app,
    width=320,
    text="Register",
    command=register
)
register_btn.pack(pady=30)

app.mainloop()