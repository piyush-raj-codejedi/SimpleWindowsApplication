"""Sidebar navigation with journey history preview."""
import tkinter as tk
from tkinter import ttk


class Sidebar(ttk.Frame):
    SIDEBAR_WIDTH = 220

    def __init__(self, parent, controller):
        super().__init__(parent, style="Card.TFrame", width=self.SIDEBAR_WIDTH)
        self.controller = controller
        self.pack_propagate(False)  # keep width

        self._build_nav()
        self._build_bookings_list()

    def _build_nav(self):
        nav = ttk.Frame(self, style="Card.TFrame", padding=(12, 16, 12, 8))
        nav.pack(fill="x")

        ttk.Label(nav, text="TestSky", font=("Segoe UI", 16, "bold"), foreground="#1a1a2e", background="white").pack(
            pady=(0, 16)
        )

        buttons = [
            ("Home", self.controller.show_home),
            ("Profile", self.controller.show_profile),
            ("Journey History", self.controller.show_journey_history),
            ("Logout", self.controller.logout),
        ]

        for text, cmd in buttons:
            style = "Danger.TButton" if text == "Logout" else "Primary.TButton"
            btn = ttk.Button(nav, text=text, style=style, width=20, command=cmd)
            btn.pack(fill="x", pady=3)

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=12, pady=8)

        ttk.Label(self, text="Recent Bookings", font=("Segoe UI", 10, "bold"), foreground="#555", background="white").pack(
            padx=12, pady=(0, 4)
        )

    def _build_bookings_list(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=(12, 0))
        frame.pack(fill="both", expand=True)

        self.bookings_listbox = tk.Listbox(frame, font=("Segoe UI", 9), bg="white", bd=0, highlightthickness=0)
        self.bookings_listbox.pack(fill="both", expand=True)

    def refresh_bookings(self):
        self.bookings_listbox.delete(0, tk.END)
        for b in reversed(self.controller.bookings[-10:]):  # show last 10
            entry = f"{b.booking_id}\n{b.flight.origin}\u2192{b.flight.destination}"
            self.bookings_listbox.insert(tk.END, entry)
