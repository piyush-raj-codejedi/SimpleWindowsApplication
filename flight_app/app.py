"""Main entry point for the TestSky flight booking application."""
import tkinter as tk
from tkinter import ttk, messagebox

from models import HARDCODED_USERS, User, Booking
from login_page import LoginPage
from booking_page import BookingPage
from profile_page import ProfilePage
from sidebar import Sidebar


class App:
    """Main application controller."""

    # ── Color Palette ──
    COLOR_PRIMARY = "#1e3a5f"
    COLOR_PRIMARY_LIGHT = "#2c5f9e"
    COLOR_ACCENT = "#48cae4"
    COLOR_SUCCESS = "#27ae60"
    COLOR_DANGER = "#e74c3c"
    COLOR_BG = "#f4f6f9"
    COLOR_CARD = "#ffffff"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TestSky — Flight Booking")
        self.root.geometry("1180x720")
        self.root.minsize(960, 640)

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        self._configure_style(style)

        # State
        self.current_user = None
        self.bookings = []  # list of Booking

        # Container
        self.container = tk.Frame(self.root, bg=self.COLOR_BG)
        self.container.pack(fill="both", expand=True)

        self.main_content = tk.Frame(self.container, bg=self.COLOR_BG)
        self.main_content.pack(side="left", fill="both", expand=True)

        # Status bar
        self.status_var = tk.StringVar(value="TestSky — Welcome")
        self.status_bar = ttk.Label(self.container, textvariable=self.status_var,
                                    style="Status.TLabel", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

        self.sidebar = Sidebar(self.container, self)
        self.sidebar.pack(side="right", fill="y", padx=8, pady=8)
        self.sidebar.pack_forget()

        # Pages
        self.login_page = LoginPage(self.main_content, self)
        self.booking_page = BookingPage(self.main_content, self)
        self.profile_page = ProfilePage(self.main_content, self)

        self._current_page = None
        self.show_login()

    @staticmethod
    def _configure_style(style):
        style.configure("TFrame", background="#f4f6f9")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground="#1e3a5f")
        style.configure("Sub.TLabel", font=("Segoe UI", 10, "normal"), foreground="#666")
        style.configure("Card.TLabel", font=("Segoe UI", 10), foreground="#333")
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Status.TLabel", font=("Segoe UI", 9), foreground="#888", padding=(8, 3))

        style.configure("Treeview", font=("Segoe UI", 9), rowheight=30, fieldbackground="#fff",
                        background="#fff", foreground="#333")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"),
                        foreground="#1e3a5f")

        for style_name, active, base in [
            ("Primary.TButton", "#1a5276", "#1e3a5f"),
            ("Success.TButton", "#1e8449", "#27ae60"),
            ("Danger.TButton", "#c0392b", "#e74c3c"),
            ("Accent.TButton", "#1abc9c", "#16a085"),
        ]:
            style.map(style_name,
                      background=[("active", active), ("!disabled", base)],
                      foreground=[("active", "#fff"), ("!disabled", "#fff")])

        # Alternate row colours
        style.configure("Treeview", background="#fff", foreground="#333", fieldbackground="#f8f9fa")
        style.map("Treeview", background=[("selected", "#d4efdf")], foreground=[("selected", "#1e3a5f")])

    def run(self):
        self.root.mainloop()

    # ── Navigation ──

    def _clear_page(self):
        if self._current_page:
            self._current_page.pack_forget()
            self._current_page = None

    def show_login(self):
        self._clear_page()
        self.sidebar.pack_forget()
        self.login_page.pack(fill="both", expand=True)
        self._current_page = self.login_page
        self.status_var.set("Login")

    def show_home(self):
        self._clear_page()
        self.sidebar.pack(side="right", fill="y", padx=8, pady=8)
        self.booking_page.reset()
        self.booking_page.pack(fill="both", expand=True, padx=8, pady=8)
        self._current_page = self.booking_page
        self.root.title("TestSky — Home")
        self.status_var.set("Home — Search & Book Flights")

    def show_profile(self):
        self._clear_page()
        self.sidebar.pack(side="right", fill="y", padx=8, pady=8)
        self.profile_page.refresh()
        self.profile_page.pack(fill="both", expand=True, padx=8, pady=8)
        self._current_page = self.profile_page
        self.root.title("TestSky — Profile")
        self.status_var.set("Profile")

    def show_journey_history(self):
        self._clear_page()
        self.sidebar.pack(side="right", fill="y", padx=8, pady=8)
        self.booking_page.show_history()
        self.booking_page.pack(fill="both", expand=True, padx=8, pady=8)
        self._current_page = self.booking_page
        self.root.title("TestSky — Journey History")
        self.status_var.set("Journey History")

    # ── Auth ──

    def login(self, username, password):
        user_data = HARDCODED_USERS.get(username)
        if user_data and user_data["password"] == password:
            self.current_user = User(username, user_data)
            self.show_home()
        else:
            messagebox.showerror("Login Failed",
                                 "Invalid username or password.\n\n"
                                 "Try demo / demo")

    def logout(self):
        self.current_user = None
        self.show_login()
        messagebox.showinfo("Logged Out",
                            "You have been logged out successfully.")

    # ── Bookings ──

    def add_booking(self, booking):
        self.bookings.append(booking)
        self.sidebar.refresh_bookings()


if __name__ == "__main__":
    import sys
    print("TestSky — Flight Booking Application", flush=True)
    app = App()
    # Force window to front
    app.root.attributes("-topmost", True)
    app.root.after(100, lambda: app.root.attributes("-topmost", False))
    print(f"Window: {app.root.winfo_geometry()}", flush=True)
    try:
        app.run()
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()
        input("Press Enter to close...")
        sys.exit(1)
