"""Sidebar navigation with journey history preview."""
import tkinter as tk
from tkinter import ttk


class Sidebar(ttk.Frame):
    SIDEBAR_WIDTH = 200

    def __init__(self, parent, controller):
        super().__init__(parent, style="Card.TFrame", width=self.SIDEBAR_WIDTH)
        self.controller = controller
        self.pack_propagate(False)

        self._build_nav()
        self._build_bookings_list()

    def _build_nav(self):
        nav = ttk.Frame(self, style="Card.TFrame", padding=(10, 14, 10, 8))
        nav.pack(fill="x")

        tk.Label(nav, text="\u2708\uFE0F TestSky", font=("Segoe UI", 14, "bold"),
                 fg="#1e3a5f", bg="#ffffff").pack(pady=(4, 14))

        buttons = [
            ("Home", self.controller.show_home),
            ("Profile", self.controller.show_profile),
            ("Journey History", self.controller.show_journey_history),
            ("Logout", self.controller.logout),
        ]

        for text, cmd in buttons:
            if text == "Logout":
                style_name = "Danger.TButton"
            else:
                style_name = "Primary.TButton"
            btn = ttk.Button(nav, text=text, style=style_name, width=20,
                             command=cmd)
            btn.pack(fill="x", pady=3)

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=10, pady=8)

        ttk.Label(self, text="Recent Bookings", font=("Segoe UI", 9, "bold"),
                  foreground="#555", background="white").pack(
            padx=10, pady=(0, 6))

    def _build_bookings_list(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=(10, 0))
        frame.pack(fill="both", expand=True)

        self.bookings_listbox = tk.Listbox(frame, font=("Segoe UI", 8),
                                           bg="#f8f9fa", borderwidth=1,
                                           relief="flat")
        self.bookings_listbox.pack(fill="both", expand=True)

    def refresh_bookings(self):
        self.bookings_listbox.delete(0, tk.END)
        for b in reversed(self.controller.bookings[-15:]):  # show last 15
            entry = (f"[{b.booking_id}]  "
                     f"{b.flight.origin} \u2192 {b.flight.destination}  "
                     f"(${b.flight.price})")
            self.bookings_listbox.insert(tk.END, entry)
