"""Booking page UI — flight search, booking, and journey history view."""
import tkinter as tk
from tkinter import ttk, messagebox

from models import CITIES, Booking, generate_flights


class BookingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_flight = None

        self._build_search()
        self._build_results()
        self._build_history()

    def _build_search(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=20)
        frame.pack(fill="x", padx=0, pady=(0, 10))

        ttk.Label(frame, text="Book a Flight", style="Header.TLabel").pack(anchor="w")

        row = ttk.Frame(frame)
        row.pack(fill="x", pady=(12, 0))

        # From
        f1 = ttk.Frame(row)
        f1.pack(side="left", fill="x", expand=True)
        ttk.Label(f1, text="From", style="Card.TLabel").pack(anchor="w")
        self.from_city = ttk.Combobox(f1, values=sorted(CITIES), state="readonly", font=("Segoe UI", 10), width=22)
        self.from_city.pack(fill="x", pady=(2, 0))

        # Arrow
        ttk.Label(row, text="  \u27A4  ", style="Sub.TLabel", foreground="#2980b9").pack(side="left")

        # To
        f2 = ttk.Frame(row)
        f2.pack(side="left", fill="x", expand=True)
        ttk.Label(f2, text="To", style="Card.TLabel").pack(anchor="w")
        self.to_city = ttk.Combobox(f2, values=sorted(CITIES), state="readonly", font=("Segoe UI", 10), width=22)
        self.to_city.pack(fill="x", pady=(2, 0))

        # Date
        date_row = ttk.Frame(frame)
        date_row.pack(fill="x", pady=(10, 0))
        ttk.Label(date_row, text="Travel Date", style="Card.TLabel").pack(anchor="w")
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(date_row, textvariable=self.date_var, font=("Segoe UI", 10), width=24)
        self.date_entry.pack(fill="x", pady=(2, 0))
        ttk.Label(date_row, text="(YYYY-MM-DD)", style="Sub.TLabel", foreground="#888").pack(anchor="w")

        # Search button
        btn_row = ttk.Frame(frame)
        btn_row.pack(fill="x", pady=(12, 0))
        ttk.Button(btn_row, text="Search Flights", style="Primary.TButton", command=self.search, width=22).pack(
            side="right"
        )

    def _build_results(self):
        results_frame = ttk.Frame(self, style="Card.TFrame", padding=20)
        results_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.results_frame = results_frame

        self.results_header = ttk.Label(results_frame, text="Search Results", style="Header.TLabel")
        self.results_header.pack(anchor="w")

        cols = ("Airline", "Flight #", "Date", "Departs", "Arrives", "Price")
        self.results_tree = ttk.Treeview(results_frame, columns=cols, show="headings", height=8)
        for c in cols:
            self.results_tree.heading(c, text=c)
            self.results_tree.column(c, width=110, anchor="center")
        self.results_tree.column("Airline", width=140)
        self.results_tree.column("Price", width=80)
        self.results_tree.pack(fill="both", expand=True, pady=(8, 0))

        self.results_tree.bind("<ButtonRelease-1>", self.on_select)
        self.results_tree.tag_configure("selected", background="#d4efdf")

        book_btn = ttk.Button(results_frame, text="Book Selected Flight", style="Success.TButton", command=self.book)
        book_btn.pack(side="right", pady=(8, 0))
        self.book_btn = book_btn

    def _build_history(self):
        history_frame = ttk.Frame(self, style="Card.TFrame", padding=20)
        self.history_frame = history_frame

        ttk.Label(history_frame, text="Journey History", style="Header.TLabel").pack(anchor="w")

        h_cols = ("Booking ID", "Airline", "Flight #", "Route", "Date", "Status")
        self.history_tree = ttk.Treeview(history_frame, columns=h_cols, show="headings", height=12)
        for c in h_cols:
            self.history_tree.heading(c, text=c)
            self.history_tree.column(c, width=100, anchor="center")
        self.history_tree.column("Airline", width=140)
        self.history_tree.column("Route", width=200)
        self.history_tree.column("Booking ID", width=100)
        self.history_tree.pack(fill="both", expand=True, pady=(8, 0))

        self.back_btn = ttk.Button(history_frame, text="Back to Search", style="Primary.TButton", command=lambda: self._toggle_view(False))
        self.back_btn.pack(side="right", pady=(8, 0))

    def _toggle_view(self, show_history):
        if show_history:
            self.results_frame.pack_forget()
            self.history_frame.pack(fill="both", expand=True, pady=(0, 10))
        else:
            self.history_frame.pack_forget()
            self._repack_results()

    def _repack_results(self):
        self.results_frame.pack(fill="both", expand=True, pady=(0, 10))

    def show_history(self):
        self._toggle_view(True)
        self.refresh_history()

    def refresh_history(self):
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)
        for b in self.controller.bookings:
            self.history_tree.insert(
                "", "end",
                values=(
                    b.booking_id,
                    b.flight.airline,
                    b.flight.flight_id,
                    f"{b.flight.origin} \u2192 {b.flight.destination}",
                    b.flight.date,
                    b.status,
                ),
            )

    def reset(self):
        self._toggle_view(False)
        self.from_city.set("")
        self.to_city.set("")
        self.date_var.set("")
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)
        self.selected_flight = None

    def search(self):
        origin = self.from_city.get()
        destination = self.to_city.get()
        date = self.date_var.get().strip()

        if not origin or not destination or not date:
            messagebox.showwarning("Incomplete", "Please fill in From, To, and Date.")
            return
        if origin == destination:
            messagebox.showwarning("Same City", "From and To cities must be different.")
            return

        # Generate flights
        flights = generate_flights(origin, destination, date)

        # Clear tree
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)

        for f in flights:
            self.results_tree.insert(
                "", "end",
                values=(f.airline, f.flight_id, f.date, f.departure_time, f.arrival_time, f"${f.price}"),
                tags=(f,),
            )

        self.results_header.config(text=f"Flights: {origin} \u2192 {destination}  ({date})")

    def on_select(self, event):
        sel = self.results_tree.selection()
        if not sel:
            return
        item = self.results_tree.item(sel[0])
        self.selected_flight = item["tags"][0]

        # Highlight
        for row in self.results_tree.get_children():
            self.results_tree.item(row, tags=())
        self.results_tree.item(sel[0], tags=("selected",))

    def book(self):
        if not self.selected_flight:
            messagebox.showwarning("No Selection", "Please select a flight first.")
            return

        flight = self.selected_flight
        user = self.controller.current_user

        booking = Booking(
            user=user,
            flight=flight,
            passenger_name=user.name,
        )

        self.controller.add_booking(booking)

        messagebox.showinfo(
            "Booking Confirmed",
            f"Booking ID: {booking.booking_id}\n"
            f"Passenger: {booking.passenger_name}\n"
            f"Flight: {flight.airline} {flight.flight_id}\n"
            f"Route: {flight.origin} \u2192 {flight.destination}\n"
            f"Date: {flight.date}  |  {flight.departure_time} - {flight.arrival_time}\n"
            f"Price: ${flight.price}\n"
            f"Status: {booking.status}",
        )

        self.selected_flight = None
