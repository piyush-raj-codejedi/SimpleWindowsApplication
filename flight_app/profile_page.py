"""Profile page UI."""
import tkinter as tk
from tkinter import ttk


class ProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = controller

        card = ttk.Frame(self, style="Card.TFrame", padding=32)
        card.place(relx=0.5, rely=0.42, anchor="center")

        # Avatar placeholder
        avatar_outer = tk.Frame(card, bg="#1e3a5f", width=72, height=72,
                                border=2)
        avatar_outer.pack(pady=(16, 12))
        avatar_outer.pack_propagate(False)

        self.user_initial = tk.Label(avatar_outer, text="",
                                     font=("Segoe UI", 28, "bold"),
                                     fg="#ffffff", bg="#1e3a5f")
        self.user_initial.pack(expand=True)

        self.title = ttk.Label(card, text="My Profile", style="Header.TLabel")
        self.title.pack(anchor="w")
        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=14)

        self.fields = {}
        for key in ("Full Name", "Username", "Email", "Total Bookings"):
            r = ttk.Frame(card)
            r.pack(fill="x", pady=(6, 2))
            ttk.Label(r, text=":", style="Card.TLabel", width=16,
                      foreground="#888",
                      font=("Segoe UI", 9, "bold")).pack(side="left")
            val = ttk.Label(r, text="", font=("Segoe UI", 10),
                            foreground="#333", style="Card.TLabel")
            val.pack(side="left", fill="x", expand=True)
            self.fields[key] = (r, val)

    def refresh(self):
        user = self.controller.current_user
        if not user:
            return
        self.user_initial.config(text=user.name[0].upper())

        labels = {
            "Full Name": user.name,
            "Username": user.username,
            "Email": user.email,
            "Total Bookings": str(len(self.controller.bookings)),
        }
        for key, val in labels.items():
            label_widget = self.fields[key][1]
            label_widget.config(text=f"  {val}")

    def pack(self, **kwargs):
        self.refresh()
        super().pack(**kwargs)
