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

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TestSky — Flight Booking")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        self._configure_style(style)

        # State
        self.current_user = None
        self.bookings = []  # list of Booking

        # Container frames
        self.container = tk.Frame(self.root, bg="#f0f2f5")
        self.container.pack(fill="both", expand=True)

        self.main_content = tk.Frame(self.container, bg="#f0f2f5")
        self.main_content.pack(side="left", fill="both", expand=True)

        self.sidebar = Sidebar(self.container, self)
        self.sidebar.pack(side="right", fill="y", padx=8, pady=8)
        self.sidebar.pack_forget()  # hidden by default

        # Pages
        self.login_page = LoginPage(self.main_content, self)
        self.booking_page = BookingPage(self.main_content, self)
        self.profile_page = ProfilePage(self.main_content, self)

        self._current_page = None
        self.show_login()

        # Centre window
        self.root.eval("tk::PlaceWindow . center")

    @staticmethod
    def _configure_style(style):
        style.configure("TFrame", background="#f0f2f5")
        style.configure("Card.TFrame", background="white", borderwidth=1)
        style.configure("Header.TLabel", font=("Segoe UI", 22, "bold"), foreground="#1a1a2e")
        style.configure("Sub.TLabel", font=("Segoe UI", 11), foreground="#555")
        style.configure("Card.TLabel", font=("Segoe UI", 10), foreground="#333")
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), foreground="#fff")
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        # Accent button colours
        style.map("Primary.TButton",
                  background=[("active", "#1a5276"), ("!disabled", "#2980b9")],
                  foreground=[("active", "#fff"), ("!disabled", "#fff")])
        style.map("Success.TButton",
                  background=[("active", "#1e8449"), ("!disabled", "#27ae60")],
                  foreground=[("active", "#fff"), ("!disabled", "#fff")])
        style.map("Danger.TButton",
                  background=[("active", "#c0392b"), ("!disabled", "#e74c3c")],
                  foreground=[("active", "#fff"), ("!disabled", "#fff")])

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
        self.login_page.pack(fill="both", expand=True, padx=20, pady=40)
        self._current_page = self.login_page

    def show_home(self):
        self._clear_page()
        self.sidebar.pack(side="right", fill="y", padx=8, pady=8)
        self.booking_page.reset()
        self.booking_page.pack(fill="both", expand=True, padx=10, pady=10)
        self._current_page = self.booking_page
        self.root.title("TestSky — Home")

    def show_profile(self):
        self._clear_page()
        self.sidebar.pack(side="right", fill="y", padx=8, pady=8)
        self.profile_page.refresh()
        self.profile_page.pack(fill="both", expand=True, padx=10, pady=10)
        self._current_page = self.profile_page
        self.root.title("TestSky — Profile")

    def show_journey_history(self):
        self._clear_page()
        self.sidebar.pack(side="right", fill="y", padx=8, pady=8)
        self.booking_page.show_history()
        self.booking_page.pack(fill="both", expand=True, padx=10, pady=10)
        self._current_page = self.booking_page
        self.root.title("TestSky — Journey History")

    # ── Auth ──

    def login(self, username, password):
        user_data = HARDCODED_USERS.get(username)
        if user_data and user_data["password"] == password:
            self.current_user = User(username, user_data)
            self.show_home()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.\n\nTry: demo / demo")

    def logout(self):
        self.current_user = None
        self.show_login()
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")

    # ── Bookings ──

    def add_booking(self, booking):
        self.bookings.append(booking)
        self.sidebar.refresh_bookings()


if __name__ == "__main__":
    app = App()
    app.run()
