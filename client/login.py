import customtkinter as ctk
from tkinter import messagebox

from modules.auth import login_user

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class LoginWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("RealTime Chat")
        self.geometry("900x550")
        self.resizable(False, False)

        # ---------------- LEFT ---------------- #

        left = ctk.CTkFrame(self, width=350, corner_radius=0)
        left.pack(side="left", fill="y")

        ctk.CTkLabel(
            left,
            text="💬\nRealTime Chat",
            font=("Segoe UI", 30, "bold")
        ).place(relx=0.5, rely=0.35, anchor="center")

        ctk.CTkLabel(
            left,
            text="Connect with everyone.\nAnytime. Anywhere.",
            font=("Segoe UI", 15)
        ).place(relx=0.5, rely=0.55, anchor="center")

        # ---------------- RIGHT ---------------- #

        right = ctk.CTkFrame(self, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(
            right,
            text="Welcome Back 👋",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(80, 20))

        self.username = ctk.CTkEntry(
            right,
            width=320,
            height=45,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(
            right,
            width=320,
            height=45,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        ctk.CTkButton(
            right,
            text="Login",
            width=320,
            height=45,
            command=self.login
        ).pack(pady=25)

        register = ctk.CTkLabel(
            right,
            text="New User? Register",
            text_color="#4EA1FF",
            cursor="hand2"
        )
        register.pack()

        register.bind("<Button-1>", self.open_register)

    # ---------------- LOGIN ---------------- #

    def login(self):

        username = self.username.get().strip()
        password = self.password.get()

        if username == "" or password == "":
            messagebox.showerror(
                "Error",
                "Please enter username and password."
            )
            return

        if login_user(username, password):

            self.destroy()

            from client.dashboard import open_dashboard

            open_dashboard(username)

        else:

            messagebox.showerror(
                "Error",
                "Invalid username or password."
            )

    # ---------------- REGISTER ---------------- #

    def open_register(self, event=None):

        self.destroy()

        from client.register import RegisterWindow

        RegisterWindow().mainloop()


def start_login():

    LoginWindow().mainloop()


if __name__ == "__main__":
    start_login()