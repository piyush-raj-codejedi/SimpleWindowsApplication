"""Login page UI."""
import tkinter as tk
from tkinter import ttk


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = controller

        # ── Banner ──
        banner = tk.Frame(self, bg="#1e3a5f", height=140)
        banner.pack(fill="x", side="top")
        banner.pack_propagate(False)

        tk.Label(banner, text="\u2708\uFE0F", font=("Segoe UI", 48),
                 bg="#1e3a5f", fg="#ffffff").pack(pady=(12, 0))
        tk.Label(banner, text="TestSky", font=("Segoe UI", 24, "bold"),
                 bg="#1e3a5f", fg="#ffffff").pack()
        tk.Label(banner, text="Flight Booking System", font=("Segoe UI", 10),
                 bg="#1e3a5f", fg="#88cae4").pack(pady=(2, 16))

        # ── Login Card ──
        card_outer = tk.Frame(self, bg="#d0d8e8", bd=2)
        card_outer.place(relx=0.5, rely=0.62, anchor="center")

        card_inner = tk.Frame(card_outer, bg="#ffffff", bd=0)
        card_inner.pack(padx=3, pady=3, fill="both", expand=True)

        card = ttk.Frame(card_inner, padding=(36, 30, 36, 24), style="Card.TFrame")
        card.pack(fill="both", expand=True)

        ttk.Label(card, text="Sign In", font=("Segoe UI", 16, "bold"),
                  foreground="#1e3a5f").pack(pady=(0, 20))

        # Username
        u_lbl = ttk.Label(card, text="\U0001F464  Username", style="Card.TLabel",
                          foreground="#555", font=("Segoe UI", 9))
        u_lbl.pack(anchor="w")
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(card, textvariable=self.username_var,
                                        font=("Segoe UI", 11))
        self.username_entry.pack(fill="x", ipady=8, pady=(2, 14))

        # Password
        p_lbl = ttk.Label(card, text="\U0001F512  Password", style="Card.TLabel",
                          foreground="#555", font=("Segoe UI", 9))
        p_lbl.pack(anchor="w")
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(card, textvariable=self.password_var,
                                        show="*", font=("Segoe UI", 11))
        self.password_entry.pack(fill="x", ipady=8, pady=(2, 14))
        self.password_entry.bind("<Return>", lambda e: self._login())

        # Sign In Button
        ttk.Button(card, text="Sign In  \u279C", style="Primary.TButton",
                   command=self._login).pack(fill="x", ipady=6, pady=(4, 16))

        # Demo accounts hint
        ttk.Label(card, text="Demo accounts:", font=("Segoe UI", 8),
                  foreground="#999").pack()
        hints = [
            "admin  /  admin123",
            "demo  /  demo",
            "piyush  /  flight2024",
        ]
        for h in hints:
            ttk.Label(card, text=h, font=("Segoe UI", 8, "bold"),
                      foreground="#1e3a5f").pack(pady=1)

        # Focus
        self.username_entry.focus()

    def _login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            return
        self.controller.login(username, password)

    def reset(self):
        self.username_var.set("")
        self.password_var.set("")
