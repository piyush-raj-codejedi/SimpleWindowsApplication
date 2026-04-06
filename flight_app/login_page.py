"""Login page UI."""
import tkinter as tk
from tkinter import ttk


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Card
        card = ttk.Frame(self, style="Card.TFrame", padding=40)
        card.place(relx=0.5, rely=0.42, anchor="center")

        # Title
        title = ttk.Label(card, text="TestSky", style="Header.TLabel")
        title.pack(pady=(0, 4))
        sub = ttk.Label(card, text="Flight Booking System", style="Sub.TLabel")
        sub.pack(pady=(0, 24))

        # Username
        ttk.Label(card, text="Username", style="Card.TLabel").pack(anchor="w")
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(card, textvariable=self.username_var, font=("Segoe UI", 11), width=28)
        self.username_entry.pack(pady=(2, 12), ipady=6)

        # Password
        ttk.Label(card, text="Password", style="Card.TLabel").pack(anchor="w")
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(card, textvariable=self.password_var, show="*", font=("Segoe UI", 11), width=28)
        self.password_entry.pack(pady=(2, 12), ipady=6)
        self.password_entry.bind("<Return>", lambda e: self.on_login())

        # Button
        btn = ttk.Button(card, text="Sign In", style="Primary.TButton", command=self.on_login, width=28)
        btn.pack(pady=(8, 16))

        # Hint
        hint = ttk.Label(
            card,
            text="Demo accounts: admin / admin123  |  demo / demo  |  piyush / flight2024",
            style="Sub.TLabel",
            foreground="#888",
            wraplength=360,
        )
        hint.pack()

    def on_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            return
        self.controller.login(username, password)

    def reset(self):
        self.username_var.set("")
        self.password_var.set("")
