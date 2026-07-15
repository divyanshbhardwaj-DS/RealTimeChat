import customtkinter as ctk
import socket
import threading
from datetime import datetime

from client.components import ChatBubble, OnlineUser

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class Dashboard(ctk.CTk):

    def __init__(self, username):

        super().__init__()

        self.username = username

        self.title(f"RealTime Chat - {username}")
        self.geometry("1100x650")
        self.minsize(1000, 600)

        # ---------------- SOCKET ---------------- #

        self.HOST = "127.0.0.1"
        self.PORT = 5000

        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.client.connect((self.HOST, self.PORT))
        self.client.sendall(username.encode())

        # ---------------- HEADER ---------------- #

        header = ctk.CTkFrame(
            self,
            height=60,
            corner_radius=0
        )
        header.pack(fill="x")

        self.title_label = ctk.CTkLabel(
            header,
            text=f"💬 RealTime Chat   |   {username}",
            font=("Segoe UI", 22, "bold")
        )

        self.title_label.pack(
            side="left",
            padx=20,
            pady=15
        )

        self.logout_btn = ctk.CTkButton(
            header,
            text="Logout",
            width=120,
            command=self.logout
        )

        self.logout_btn.pack(
            side="right",
            padx=20
        )

        # ---------------- BODY ---------------- #

        body = ctk.CTkFrame(self)
        body.pack(fill="both", expand=True)

        # ---------------- USERS ---------------- #

        self.users_frame = ctk.CTkFrame(
            body,
            width=220
        )

        self.users_frame.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )

        self.users_title = ctk.CTkLabel(
            self.users_frame,
            text="🟢 Online Users",
            font=("Segoe UI",18,"bold")
        )

        self.users_title.pack(
            pady=15
        )

        # ---------------- CHAT ---------------- #

        self.chat_container = ctk.CTkScrollableFrame(
            body,
            corner_radius=10
        )

        self.chat_container.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ---------------- BOTTOM ---------------- #

        bottom = ctk.CTkFrame(self)
        bottom.pack(fill="x")

        self.message_entry = ctk.CTkEntry(
            bottom,
            placeholder_text="Type message...",
            height=42
        )

        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
            pady=15
        )

        self.message_entry.bind(
            "<Return>",
            lambda e: self.send_message()
        )

        send_btn = ctk.CTkButton(
            bottom,
            text="Send",
            width=120,
            command=self.send_message
        )

        send_btn.pack(
            side="right",
            padx=15
        )

        threading.Thread(
            target=self.receive_messages,
            daemon=True
        ).start()
        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )
            # ---------------- SEND MESSAGE ---------------- #

    def send_message(self):

        message = self.message_entry.get().strip()

        if message == "":
            return

        current_time = datetime.now().strftime("%I:%M %p")

        full_message = f"[{current_time}] {self.username}: {message}"

        try:
            self.client.sendall(full_message.encode())

            bubble = ChatBubble(
                self.chat_container,
                full_message,
                own=True
            )

            bubble.pack(
                anchor="e",
                padx=10,
                pady=5
            )

            self.chat_container._parent_canvas.yview_moveto(1.0)

        except Exception as e:
            print(e)

        self.message_entry.delete(0, "end")



    # ---------------- RECEIVE ---------------- #

    def receive_messages(self):

        while True:

            try:

                message = self.client.recv(1024).decode()

                if not message:
                    break

                if message.startswith("USERS:"):

                    users = message.replace(
                        "USERS:",
                        ""
                    )

                    self.after(
                        0,
                        lambda u=users: self.update_users(u)
                    )

                else:

                    self.after(
                        0,
                        lambda m=message: self.add_message(m)
                    )

            except Exception as e:

                print(e)

                break



    # ---------------- ADD MESSAGE ---------------- #

    def add_message(self, message):

        bubble = ChatBubble(
            self.chat_container,
            message,
            own=False
        )

        bubble.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        self.chat_container._parent_canvas.yview_moveto(1.0)



    # ---------------- ONLINE USERS ---------------- #

    def update_users(self, users):

        for widget in self.users_frame.winfo_children():

            if widget != self.users_title:
                widget.destroy()

        if users.strip() == "":
            return

        for user in users.split(","):

            user = user.strip()

            if user == "":
                continue

            item = OnlineUser(
                self.users_frame,
                user
            )

            item.pack(
                fill="x",
                pady=2
            )

                # ---------------- LOGOUT ---------------- #

    def logout(self):

        try:
            self.client.shutdown(socket.SHUT_RDWR)
        except:
            pass

        try:
            self.client.close()
        except:
            pass

        self.destroy()

        from client.login import start_login
        start_login()



    # ---------------- WINDOW CLOSE ---------------- #

    def on_close(self):

        try:
            self.client.shutdown(socket.SHUT_RDWR)
        except:
            pass

        try:
            self.client.close()
        except:
            pass

        self.destroy()


def open_dashboard(username):
    Dashboard(username).mainloop()