"""Profile page UI."""
import tkinter as tk
from tkinter import ttk


class ProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        card = ttk.Frame(self, style="Card.TFrame", padding=30)
        card.place(relx=0.5, rely=0.35, anchor="center")

        self.title = ttk.Label(card, text="My Profile", style="Header.TLabel")
        self.title.pack(anchor="w")

        sep = ttk.Separator(card, orient="horizontal")
        sep.pack(fill="x", pady=12)

        self.name_label = ttk.Label(card, style="Card.TLabel")
        self.name_label.pack(anchor="w", pady=(4, 2))

        self.username_label = ttk.Label(card, style="Card.TLabel")
        self.username_label.pack(anchor="w", pady=(4, 2))

        self.email_label = ttk.Label(card, style="Card.TLabel")
        self.email_label.pack(anchor="w", pady=(4, 2))

        self.stats_label = ttk.Label(card, style="Card.TLabel")
        self.stats_label.pack(anchor="w", pady=(16, 8))

    def refresh(self):
        user = self.controller.current_user
        if not user:
            return
        bookings = self.controller.bookings
        self.name_label.config(text=f"Name:  {user.name}")
        self.username_label.config(text=f"Username:  {user.username}")
        self.email_label.config(text=f"Email:  {user.email}")
        self.stats_label.config(
            text=f"Total Bookings:  {len(bookings)}"
        )

    def pack(self, **kwargs):
        self.refresh()
        super().pack(**kwargs)
