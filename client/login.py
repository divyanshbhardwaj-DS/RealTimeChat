import customtkinter as ctk

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

login_btn = ctk.CTkButton(
    right_frame,
    text="Login",
    width=320,
    height=45
)
login_btn.pack(pady=25)

register_label = ctk.CTkLabel(
    right_frame,
    text="New User? Register",
    text_color="#4EA1FF",
    cursor="hand2"
)
register_label.pack()

app.mainloop()