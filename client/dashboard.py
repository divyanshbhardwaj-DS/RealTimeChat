import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class Dashboard(ctk.CTk):

    def __init__(self, username):
        import socket
        import threading
        super().__init__()

        self.username = username

        self.title(f"RealTime Chat - {username}")
        self.geometry("900x600")

        # ---------- Header ----------
        HOST = "127.0.0.1"
        PORT = 5000

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        header = ctk.CTkFrame(self, height=60)
        header.pack(fill="x")

        title = ctk.CTkLabel(
            header,
            text=f"💬 RealTime Chat | {username}",
            font=("Segoe UI", 22, "bold")
        )

        title.pack(pady=15)

        # ---------- Chat ----------

        self.chat_box = ctk.CTkTextbox(
            self,
            width=850,
            height=420
        )

        self.chat_box.pack(pady=15)

        self.chat_box.configure(state="disabled")

        # ---------- Bottom ----------

        bottom = ctk.CTkFrame(self)

        bottom.pack(fill="x", padx=10, pady=10)

        self.message_entry = ctk.CTkEntry(
            bottom,
            width=700,
            placeholder_text="Type message..."
        )

        self.message_entry.pack(side="left", padx=10)

        self.send_btn = ctk.CTkButton(
        bottom,
        text="Send",
        width=120,
        command=self.send_message
        )

        self.send_btn.pack(side="right", padx=10)
        threading.Thread(
        target=self.receive_messages,
        daemon=True
).start()
    def send_message(self):

        message = self.message_entry.get()

        if message == "":
            return

        self.client.send(message.encode())

        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"You : {message}\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

        self.message_entry.delete(0, "end")
    def receive_messages(self):

        while True:

            try:

                message = self.client.recv(1024).decode()

                self.chat_box.configure(state="normal")

                self.chat_box.insert("end", message + "\n")

                self.chat_box.configure(state="disabled")

                self.chat_box.see("end")

            except:

                break


def open_dashboard(username):

    app = Dashboard(username)

    app.mainloop()