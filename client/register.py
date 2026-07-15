import customtkinter as ctk
from tkinter import messagebox

from modules.auth import register_user
from modules.validators import validate_registration

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class RegisterWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Create Account")
        self.geometry("500x600")
        self.resizable(False, False)

        ctk.CTkLabel(
            self,
            text="Create Account",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=30)

        self.full_name = ctk.CTkEntry(
            self,
            width=320,
            height=40,
            placeholder_text="Full Name"
        )
        self.full_name.pack(pady=10)

        self.username = ctk.CTkEntry(
            self,
            width=320,
            height=40,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(
            self,
            width=320,
            height=40,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        self.confirm = ctk.CTkEntry(
            self,
            width=320,
            height=40,
            placeholder_text="Confirm Password",
            show="*"
        )
        self.confirm.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Register",
            width=320,
            height=45,
            command=self.register
        ).pack(pady=20)

        login_label = ctk.CTkLabel(
            self,
            text="Already have an account? Login",
            text_color="#4EA1FF",
            cursor="hand2"
        )
        login_label.pack()

        login_label.bind("<Button-1>", self.open_login)

    # ---------------- REGISTER ---------------- #

    def register(self):

        full_name = self.full_name.get().strip()
        username = self.username.get().strip()
        password = self.password.get()
        confirm = self.confirm.get()

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

            messagebox.showinfo(
                "Success",
                msg
            )

            self.destroy()

            from client.login import start_login

            start_login()

        else:

            messagebox.showerror(
                "Error",
                msg
            )

    # ---------------- LOGIN ---------------- #

    def open_login(self, event=None):

        self.destroy()

        from client.login import start_login

        start_login()


if __name__ == "__main__":
    RegisterWindow().mainloop()