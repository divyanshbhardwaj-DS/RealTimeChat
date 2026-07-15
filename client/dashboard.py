import customtkinter as ctk
import socket
import threading
from datetime import datetime


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class Dashboard(ctk.CTk):

    def __init__(self, username):

        super().__init__()


        self.username = username


        self.title(
            f"RealTime Chat - {username}"
        )

        self.geometry(
            "1000x600"
        )



        # ---------- Socket ----------

        HOST = "127.0.0.1"
        PORT = 5000


        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )


        self.client.connect(
            (HOST, PORT)
        )


        self.client.sendall(
            username.encode()
        )



        # ---------- Header ----------

        header = ctk.CTkFrame(
            self,
            height=60
        )

        header.pack(
            fill="x"
        )


        title = ctk.CTkLabel(
            header,
            text=f"💬 RealTime Chat | {username}",
            font=("Segoe UI",22,"bold")
        )

        title.pack(
            pady=15
        )



        # ---------- Main ----------

        main = ctk.CTkFrame(
            self
        )

        main.pack(
            fill="both",
            expand=True
        )



        # ---------- Chat Area ----------


        self.chat_frame = ctk.CTkScrollableFrame(
            main,
            width=700,
            height=420
        )

        self.chat_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )



        # ---------- Online Users ----------


        self.users_frame = ctk.CTkFrame(
            main,
            width=220
        )


        self.users_frame.pack(
            side="right",
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



        # ---------- Bottom ----------


        bottom = ctk.CTkFrame(
            self
        )

        bottom.pack(
            fill="x",
            padx=10,
            pady=10
        )



        self.message_entry = ctk.CTkEntry(
            bottom,
            width=750,
            placeholder_text="Type message..."
        )


        self.message_entry.pack(
            side="left",
            padx=10
        )


        self.message_entry.bind(
            "<Return>",
            lambda event:self.send_message()
        )



        send_btn = ctk.CTkButton(
            bottom,
            text="Send",
            command=self.send_message,
            width=120
        )


        send_btn.pack(
            side="right"
        )



        # ---------- Receive Thread ----------


        threading.Thread(
            target=self.receive_messages,
            daemon=True
        ).start()



    # ---------- Add Message ----------


    def add_message(
        self,
        message,
        sender="other"
    ):


        bubble = ctk.CTkFrame(
            self.chat_frame,
            corner_radius=15,
            fg_color=("#2563eb" if sender == "you" else "#3a3a3a")
        )


        if sender=="you":

            bubble.pack(
                anchor="e",
                pady=5,
                padx=10
            )

        else:

            bubble.pack(
                anchor="w",
                pady=5,
                padx=10
            )



        label = ctk.CTkLabel(
            bubble,
            text=message,
            font=("Segoe UI",14)
        )


        label.pack(
            padx=15,
            pady=8
        )
        self.chat_frame._parent_canvas.yview_moveto(1.0)



    # ---------- Update Users ----------


    def update_users(
        self,
        users
    ):


        for widget in self.users_frame.winfo_children():

            if widget != self.users_title:

                widget.destroy()



        if users:


            for user in users.split(","):


                if user:


                    label = ctk.CTkLabel(
                        self.users_frame,
                        text="🟢 "+user,
                        font=("Segoe UI",14)
                    )


                    label.pack(
                        pady=5
                    )



    # ---------- Send Message ----------


    def send_message(self):


        message = self.message_entry.get()


        if message == "":

            return



        time = datetime.now().strftime(
            "%I:%M %p"
        )


        full_message = (
            f"[{time}] {self.username}: {message}"
        )



        try:

            self.client.sendall(
                full_message.encode()
            )


            self.add_message(
                full_message,
                "you"
            )


        except:

            pass



        self.message_entry.delete(
            0,
            "end"
        )



    # ---------- Receive Messages ----------


    def receive_messages(self):


        while True:


            try:


                message = self.client.recv(
                    1024
                ).decode()



                if not message:

                    break



                if message.startswith(
                    "USERS:"
                ):


                    users = message.replace(
                        "USERS:",
                        ""
                    )


                    self.after(
                        0,
                        lambda:self.update_users(users)
                    )


                else:
                        if not message.startswith(f"[") or f"{self.username}:" not in message:
                            self.after(
                                0,
                                lambda m=message: self.add_message(m, "other")
                        )



            except Exception as e:

                print(e)

                break




def open_dashboard(username):

    app = Dashboard(username)

    app.mainloop()