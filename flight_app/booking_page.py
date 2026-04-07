"""Booking page UI — flight search, booking, calendar, and journey history."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from models import CITIES, Booking, generate_flights
from calendar_widget import DatePicker


class BookingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = controller
        self.selected_flight = None
        self.selected_iid = None
        self.view_mode = "search"
        # iid -> Flight  (used so we don't put objects in tree tags)
        self._flight_by_iid = {}

        self._build_search_panel()
        self._build_results_panel()
        self._build_history_panel()
        self._build_processing_panel()
        self._build_success_panel()

    # ── Search Panel ──

    def _build_search_panel(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=24)
        frame.pack(fill="x", padx=0, pady=(0, 8))

        header_row = ttk.Frame(frame)
        header_row.pack(fill="x")
        ttk.Label(header_row, text="Book a Flight",
                  style="Header.TLabel").pack(side="left", anchor="w")
        ttk.Separator(header_row, orient="horizontal").pack(
            side="left", fill="x", expand=True, padx=(16, 0), pady=14)

        # From / To row
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=(14, 0))

        f1 = ttk.Frame(row)
        f1.pack(side="left", fill="x", expand=True)
        ttk.Label(f1, text="From", font=("Segoe UI", 9, "bold"),
                  foreground="#555").pack(anchor="w")
        self.from_city = ttk.Combobox(f1, values=sorted(CITIES),
                                      state="readonly", font=("Segoe UI", 10))
        self.from_city.pack(fill="x", pady=(4, 0), ipady=4)

        ttk.Label(row, text="  \u27A4  ", font=("Segoe UI", 16),
                  foreground="#1e3a5f").pack(side="left")

        f2 = ttk.Frame(row)
        f2.pack(side="left", fill="x", expand=True)
        ttk.Label(f2, text="To", font=("Segoe UI", 9, "bold"),
                  foreground="#555").pack(anchor="w")
        self.to_city = ttk.Combobox(f2, values=sorted(CITIES),
                                    state="readonly", font=("Segoe UI", 10))
        self.to_city.pack(fill="x", pady=(4, 0), ipady=4)

        # Date + calendar button
        date_row = ttk.Frame(frame)
        date_row.pack(fill="x", pady=(12, 0))
        date_left = ttk.Frame(date_row)
        date_left.pack(side="left", fill="x", expand=True)
        ttk.Label(date_left, text="Travel Date", font=("Segoe UI", 9, "bold"),
                  foreground="#555").pack(anchor="w")

        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(date_left, textvariable=self.date_var,
                                    font=("Segoe UI", 10), state="readonly", width=24)
        self.date_entry.pack(fill="x", pady=(4, 0))

        self.cal_btn = ttk.Button(date_left, text="Select Date",
                                  style="Accent.TButton", command=self._open_calendar)
        self.cal_btn.pack(fill="x", pady=(8, 0))

        # Search button
        btn_row = ttk.Frame(frame)
        btn_row.pack(fill="x", pady=(14, 4))
        ttk.Button(btn_row, text="Search Flights", style="Primary.TButton",
                   command=self.search).pack(side="right")

    def _open_calendar(self):
        def on_pick(date_str):
            self.date_var.set(date_str)
        DatePicker(self, on_select=on_pick)

    # ── Results Panel ──

    def _build_results_panel(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=24)
        frame.pack(fill="both", expand=True, pady=(0, 8))
        self.results_frame = frame

        self.results_header = ttk.Label(frame, text="Search Results",
                                        style="Header.TLabel")
        self.results_header.pack(anchor="w")

        cols = ("Airline", "Flight #", "Date", "Departs", "Arrives", "Price")
        self.results_tree = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        col_widths = {"Airline": 150, "Flight #": 90, "Date": 100,
                      "Departs": 85, "Arrives": 85, "Price": 80}
        for c in cols:
            self.results_tree.heading(c, text=c)
            self.results_tree.column(c, width=col_widths.get(c, 100), anchor="center")
        self.results_tree.pack(fill="both", expand=True, pady=(10, 0))

        self.results_tree.bind("<ButtonRelease-1>", self.on_select)
        self.results_tree.tag_configure("selected", background="#d4efdf")
        self.results_tree.tag_configure("even", background="#f8f9fa")
        self.results_tree.tag_configure("odd", background="#ffffff")

        book_btn = ttk.Button(frame, text="Book Selected Flight",
                              style="Success.TButton", command=self.book)
        book_btn.pack(side="right", pady=(10, 0))

    # ── History Panel ──

    def _build_history_panel(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=24)
        self.history_frame = frame

        ttk.Label(frame, text="Journey History", style="Header.TLabel").pack(anchor="w")
        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=(6, 10))

        h_cols = ("Booking ID", "Route", "Date", "Fare", "Status")
        self.history_tree = ttk.Treeview(frame, columns=h_cols, show="headings", height=12)
        h_widths = {"Booking ID": 100, "Route": 210, "Date": 100,
                    "Fare": 80, "Status": 90}
        for c in h_cols:
            self.history_tree.heading(c, text=c)
            self.history_tree.column(c, width=h_widths.get(c, 100), anchor="center")
        self.history_tree.column("Route", anchor="w")
        self.history_tree.pack(fill="both", expand=True, pady=(0, 10))

        self.back_btn = ttk.Button(frame, text="Back to Search",
                                   style="Primary.TButton",
                                   command=lambda: self._set_view("search"))
        self.back_btn.pack(side="right")

    # ── Processing Panel ──

    def _build_processing_panel(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=40)
        self.processing_frame = frame

        self.spinner_var = tk.StringVar(value="Processing...")
        tk.Label(frame, textvariable=self.spinner_var,
                 font=("Segoe UI", 14, "bold"), bg="#ffffff",
                 foreground="#1e3a5f").pack(pady=(40, 16))

        ttk.Label(frame, text="Please wait while we confirm your booking.",
                  font=("Segoe UI", 10), foreground="#666", style="Card.TLabel").pack()

        self.spinner_frames = [
            "\u2022\u2022\u2022",
            "\u2022\u2022 \u00A0",
            "\u2022 \u00A0\u00A0",
            " \u00A0\u00A0\u00A0",
        ]
        self._spinner_idx = 0
        self._spinner_job = None

    def _start_spinner(self):
        self._spinner_idx = 0
        self._animate_spinner()

    def _animate_spinner(self):
        def tick():
            self.spinner_var.set(self.spinner_frames[self._spinner_idx])
            self._spinner_idx = (self._spinner_idx + 1) % len(self.spinner_frames)
            self._spinner_job = self.controller.root.after(150, tick)
        tick()

    def _stop_spinner(self):
        if self._spinner_job:
            self.controller.root.after_cancel(self._spinner_job)
            self._spinner_job = None

    # ── Success Panel ──

    def _build_success_panel(self):
        frame = ttk.Frame(self, style="Card.TFrame", padding=40)
        self.success_frame = frame

        tk.Label(frame, text="\u2705", font=("Segoe UI", 64),
                 bg="#ffffff").pack(pady=(30, 12))

        self.success_title = ttk.Label(frame,
                                       text="Booking Confirmed!",
                                       font=("Segoe UI", 18, "bold"),
                                       foreground="#27ae60", style="Card.TLabel")
        self.success_title.pack()

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=(12, 0))

        details = ttk.Frame(frame, style="Card.TFrame")
        details.pack(fill="x", pady=(14, 0))

        self.detail_labels = {}
        for label in ("Passenger", "Flight", "Route", "Date & Time", "Fare", "Booking ID"):
            r = ttk.Frame(details)
            r.pack(fill="x", pady=4)
            ttk.Label(r, text=f"{label}:", font=("Segoe UI", 9, "bold"),
                      foreground="#1e3a5f", width=14, style="Card.TLabel").pack(side="left")
            val = ttk.Label(r, text="", font=("Segoe UI", 10), foreground="#333",
                            style="Card.TLabel")
            val.pack(side="left", fill="x", expand=True)
            self.detail_labels[label] = val

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(20, 0))
        ttk.Button(btn_frame, text="Book Another",
                   style="Primary.TButton",
                   command=self._go_home_from_success).pack(side="right", padx=(8, 0))
        ttk.Button(btn_frame, text="Home",
                   style="Accent.TButton",
                   command=self._go_home_from_success).pack(side="right")

    def _populate_success(self, booking):
        self.detail_labels["Passenger"].config(text=booking.passenger_name)
        f = booking.flight
        self.detail_labels["Flight"].config(text=f"{f.airline}  ({f.flight_id})")
        self.detail_labels["Route"].config(text=f"{f.origin}  \u2192  {f.destination}")
        dep_arr = f"Departs {f.departure_time}  |  Arrives {f.arrival_time}"
        self.detail_labels["Date & Time"].config(text=f"{f.date}  \u2014  {dep_arr}")
        self.detail_labels["Fare"].config(text=f"${f.price}")
        self.detail_labels["Booking ID"].config(text=booking.booking_id)

    def _go_home_from_success(self):
        self.controller.show_home()

    # ── View Management ──

    def _hide_all(self):
        for fr in (self.results_frame, self.history_frame,
                   self.processing_frame, self.success_frame):
            fr.pack_forget()

    def _show_search(self):
        self.results_frame.pack(fill="both", expand=True, pady=(0, 8))

    def _set_view(self, mode):
        self.view_mode = mode
        self._hide_all()
        if mode == "search":
            self._show_search()
            self._stop_spinner()
        elif mode == "history":
            self.history_frame.pack(fill="both", expand=True, pady=(0, 8))
            self.refresh_history()
        elif mode == "processing":
            self.processing_frame.pack(fill="both", expand=True, pady=(0, 8))
            self._start_spinner()
        elif mode == "success":
            self.success_frame.pack(fill="both", expand=True, pady=(0, 8))
            self._stop_spinner()

    # ── Public API ──

    def show_history(self):
        self._set_view("history")

    def show_processing(self):
        self._set_view("processing")

    def show_success(self, booking):
        self._populate_success(booking)
        self._set_view("success")

    def reset(self):
        self._set_view("search")
        self.from_city.set("")
        self.to_city.set("")
        self.date_var.set("")
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)
        self._flight_by_iid.clear()
        self.selected_flight = None
        self.selected_iid = None

    # ── Search ──

    def search(self):
        origin = self.from_city.get()
        destination = self.to_city.get()
        date = self.date_var.get().strip()

        if not origin or not destination:
            messagebox.showwarning("Incomplete", "Please select From and To cities.")
            return
        if origin == destination:
            messagebox.showwarning("Same City",
                                   "From and To cities must be different.")
            return
        if not date:
            messagebox.showwarning("Incomplete", "Please select a travel date.")
            return

        try:
            travel_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Invalid Date",
                                 "Date must be in YYYY-MM-DD format.\n"
                                 "Use the calendar picker to select correctly.")
            return

        today = datetime.now().date()
        if travel_date < today:
            messagebox.showerror("Past Date Not Allowed",
                                 f"Selected date ({date}) is in the past.\n"
                                 "Please pick today or a future date.")
            return

        flights = generate_flights(origin, destination, date)

        for row in self.results_tree.get_children():
            self.results_tree.delete(row)
        self._flight_by_iid.clear()

        for i, f in enumerate(flights):
            tag = "even" if i % 2 == 0 else "odd"
            iid = self.results_tree.insert(
                "", "end",
                values=(f.airline, f.flight_id, f.date,
                        f.departure_time, f.arrival_time, f"${f.price}"),
                tags=(tag,),
            )
            self._flight_by_iid[iid] = f

        self.results_header.config(
            text=f"Flights: {origin}  \u2192  {destination}  ({date})")

    # ── Row selection ──

    def on_select(self, event):
        sel = self.results_tree.selection()
        if not sel:
            return
        iid = sel[0]
        self.selected_flight = self._flight_by_iid.get(iid)
        self.selected_iid = iid

        for row in self.results_tree.get_children():
            tags = list(self.results_tree.item(row)["tags"])
            if "selected" in tags:
                tags.remove("selected")
            self.results_tree.item(row, tags=tuple(tags))

        self.results_tree.item(iid, tags=["selected"])

    # ── Booking flow ──

    def book(self):
        if not self.selected_flight:
            messagebox.showwarning("No Selection",
                                   "Please select a flight first.")
            return

        flight = self.selected_flight
        user = self.controller.current_user

        booking = Booking(user=user, flight=flight, passenger_name=user.name)
        self.controller.add_booking(booking)

        # Show processing animation
        self.show_processing()

        # After 2 seconds, show success
        def show_success_deferred():
            self.show_success(booking)

        self.controller.root.after(2000, show_success_deferred)

        self.selected_flight = None
        self.selected_iid = None

    # ── History ──

    def refresh_history(self):
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)
        for b in self.controller.bookings:
            self.history_tree.insert(
                "", "end",
                values=(
                    b.booking_id,
                    f"{b.flight.origin}  \u2192  {b.flight.destination}",
                    b.flight.date,
                    f"${b.flight.price}",
                    b.status,
                ),
            )
