import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def open_dashboard(username):

    app = ctk.CTk()

    app.geometry("900x550")
    app.title("Dashboard")

    title = ctk.CTkLabel(
        app,
        text=f"Welcome {username} 👋",
        font=("Segoe UI", 28, "bold")
    )

    title.pack(pady=40)

    status = ctk.CTkLabel(
        app,
        text="🟢 Online",
        font=("Segoe UI", 18)
    )

    status.pack()

    logout = ctk.CTkButton(
        app,
        text="Logout",
        command=app.destroy
    )

    logout.pack(pady=30)

    app.mainloop()