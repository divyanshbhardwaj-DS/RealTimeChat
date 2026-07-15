import customtkinter as ctk


class ChatBubble(ctk.CTkFrame):

    def __init__(self, master, text, own=False):

        color = "#2563EB" if own else "#3A3A3A"

        super().__init__(
            master,
            fg_color=color,
            corner_radius=15
        )

        label = ctk.CTkLabel(
            self,
            text=text,
            justify="left",
            wraplength=450,
            font=("Segoe UI", 14)
        )

        label.pack(
            padx=12,
            pady=8
        )


class OnlineUser(ctk.CTkFrame):

    def __init__(self, master, username):

        super().__init__(
            master,
            fg_color="transparent"
        )

        label = ctk.CTkLabel(
            self,
            text="🟢 " + username,
            anchor="w",
            font=("Segoe UI", 14)
        )

        label.pack(
            fill="x",
            padx=10,
            pady=5
        )