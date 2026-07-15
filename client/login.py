import customtkinter as ctk
from tkinter import messagebox
from modules.auth import login_user
# ---------------- Appearance ---------------- #
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ---------------- Window ---------------- #
app = ctk.CTk()
app.title("RealTime Chat")
app.geometry("900x550")
app.resizable(False, False)

# ---------------- Left Frame ---------------- #
left_frame = ctk.CTkFrame(app, width=350, corner_radius=0)
left_frame.pack(side="left", fill="y")

title = ctk.CTkLabel(
    left_frame,
    text="💬\nRealTime Chat",
    font=("Segoe UI", 30, "bold")
)
title.place(relx=0.5, rely=0.35, anchor="center")

subtitle = ctk.CTkLabel(
    left_frame,
    text="Connect with everyone.\nAnytime. Anywhere.",
    font=("Segoe UI", 15)
)
subtitle.place(relx=0.5, rely=0.55, anchor="center")

# ---------------- Right Frame ---------------- #
right_frame = ctk.CTkFrame(app, fg_color="transparent")
right_frame.pack(side="right", fill="both", expand=True)

heading = ctk.CTkLabel(
    right_frame,
    text="Welcome Back 👋",
    font=("Segoe UI", 28, "bold")
)
heading.pack(pady=(80, 20))

username_entry = ctk.CTkEntry(
    right_frame,
    width=320,
    height=45,
    placeholder_text="Username"
)
username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(
    right_frame,
    width=320,
    height=45,
    placeholder_text="Password",
    show="*"
)
password_entry.pack(pady=10)

def open_register():
    app.destroy()

    from client.register import app as register_app
    register_app.mainloop()

# Login fxn
def login():

    username = username_entry.get().strip()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Please enter username and password.")
        return

    if login_user(username, password):
        messagebox.showinfo("Success", "Login Successful!")
        app.destroy()

        from client.dashboard import open_dashboard
        open_dashboard(username)

    else:
        messagebox.showerror("Error", "Invalid username or password.")

login_btn = ctk.CTkButton(
    right_frame,
    text="Login",
    width=320,
    height=45,
    command=login
)
login_btn.pack(pady=25)

register_label = ctk.CTkLabel(
    right_frame,
    text="New User? Register",
    text_color="#4EA1FF",
    cursor="hand2"
)
register_label.pack()
register_label.bind("<Button-1>", lambda e: open_register())
app.mainloop()