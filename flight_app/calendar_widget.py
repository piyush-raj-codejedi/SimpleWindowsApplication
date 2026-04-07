"""Calendar date picker widget built with tkinter."""
import tkinter as tk
from tkinter import ttk
import calendar as cal_module
from datetime import datetime


class DatePicker:
    """Popup calendar date picker for tkinter apps."""

    def __init__(self, parent, on_select=None):
        self.top = None
        self.on_select = on_select
        self.selected_date = None

        now = datetime.now()
        self.year = now.year
        self.month = now.month
        self.day = now.day

        # Open immediately
        self._open(parent)

    def _open(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Select Date")
        self.top.resizable(False, False)
        self.top.attributes("-topmost", True)

        # Center over parent
        x = parent.winfo_rootx() + parent.winfo_width() // 2 - 140
        y = parent.winfo_rooty() + parent.winfo_height() // 2 - 170
        self.top.geometry(f"300x340+{x}+{y}")

        self._style = ttk.Style()
        self._style.configure("CalNav.TButton", font=("Segoe UI", 11, "bold"))
        self._style.configure("CalMonth.TLabel", font=("Segoe UI", 13, "bold"), anchor="center")
        self._style.configure("CalDay.TLabel", font=("Segoe UI", 9), anchor="center")
        self._style.configure("CalToday.TLabel", font=("Segoe UI", 9, "bold"), anchor="center",
                              foreground="#2980b9")

        self._build_header()
        self._build_body()

    def _build_header(self):
        nav = ttk.Frame(self.top)
        nav.pack(fill="x", pady=(10, 4))

        prev_btn = ttk.Button(nav, text="< Prev", style="CalNav.TButton", command=self._prev_month, width=8)
        prev_btn.pack(side="left", padx=8)

        self.month_label = ttk.Label(nav, style="CalMonth.TLabel")
        self.month_label.pack(side="left", fill="x", expand=True)

        next_btn = ttk.Button(nav, text="Next >", style="CalNav.TButton", command=self._next_month, width=8)
        next_btn.pack(side="left", padx=8)

        self._refresh_month_label()

    def _build_body(self):
        # Day headers
        days = "Mon Tue Wed Thu Fri Sat Sun".split()
        hdr = ttk.Frame(self.top)
        hdr.pack(fill="x", padx=8, pady=(4, 0))
        for d in days:
            ttk.Label(hdr, text=d[0], style="CalDay.TLabel", width=3,
                      foreground="#888").pack(side="left", expand=True)

        self._day_frame = ttk.Frame(self.top)
        self._day_frame.pack(fill="both", expand=True, padx=8)

        self._render_calendar()

        # Today button
        ttk.Button(self.top, text="Today", style="CalNav.TButton",
                   command=self._select_today).pack(pady=(4, 8))

    def _render_calendar(self):
        for w in self._day_frame.winfo_children():
            w.destroy()

        matrix = cal_module.monthcalendar(self.year, self.month)
        today = datetime.now()
        self._day_labels = []

        for row_idx, week in enumerate(matrix):
            row = ttk.Frame(self._day_frame)
            row.pack(fill="x")
            for col_idx, d in enumerate(week):
                if d == 0:
                    ttk.Label(row, text="", width=3, style="CalDay.TLabel").pack(
                        side="left", expand=True, fill="both", padx=1, pady=1)
                    continue

                is_today = (self.year == today.year and self.month == today.month and d == today.day)
                st = "CalToday.TLabel" if is_today else "CalDay.TLabel"
                lbl = ttk.Label(row, text=str(d), style=st, width=3, cursor="hand2",
                                relief="flat", anchor="center")
                lbl.pack(side="left", expand=True, fill="both", padx=1, pady=1)
                lbl.bind("<Button-1>", lambda e, d=d: self._on_day_click(d))
                self._day_labels.append((d, lbl))

    def _refresh_month_label(self):
        self.month_label.config(text=f"{cal_module.month_name[self.month]} {self.year}")

    def _prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self._refresh_month_label()
        self._render_calendar()

    def _next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self._refresh_month_label()
        self._render_calendar()

    def _on_day_click(self, day):
        self.selected_date = f"{self.year}-{self.month:02d}-{day:02d}"
        if self.on_select:
            self.on_select(self.selected_date)
        self.top.destroy()

    def _select_today(self):
        today = datetime.now()
        self.selected_date = today.strftime("%Y-%m-%d")
        if self.on_select:
            self.on_select(self.selected_date)
        self.top.destroy()
