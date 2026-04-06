"""Data models for the flight booking application."""
import random
from datetime import datetime, timedelta

CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Seattle", "Denver", "Boston", "Miami", "Atlanta",
    "San Francisco", "Dallas", "Las Vegas", "Orlando", "Portland",
]

AIRLINES = [
    "Delta Airlines", "United Airlines", "American Airlines",
    "Southwest Airlines", "JetBlue Airways", "Alaska Airlines",
    "Spirit Airlines", "Frontier Airlines", "Hawaiian Airlines",
]

FLIGHT_NUMBERS = {
    "Delta Airlines": "DL{}{}",
    "United Airlines": "UA{}{}",
    "American Airlines": "AA{}{}",
    "Southwest Airlines": "WN{}{}",
    "JetBlue Airways": "B6{}{}",
    "Alaska Airlines": "AS{}{}",
    "Spirit Airlines": "NK{}{}",
    "Frontier Airlines": "F9{}{}",
    "Hawaiian Airlines": "HA{}{}",
}

HARDCODED_USERS = {
    "admin": {"password": "admin123", "name": "Admin User", "email": "admin@testsky.com"},
    "piyush": {"password": "flight2024", "name": "Piyush Raj", "email": "piyush@testsky.com"},
    "demo": {"password": "demo", "name": "Demo Account", "email": "demo@testsky.com"},
}


class User:
    """Represents a logged-in user."""

    def __init__(self, username, data):
        self.username = username
        self.name = data["name"]
        self.email = data["email"]

    def __repr__(self):
        return f"User({self.username}, {self.name})"


class Flight:
    """Represents a single flight option."""

    def __init__(self, airline, flight_id, origin, destination, date, departure_time, arrival_time, price):
        self.airline = airline
        self.flight_id = flight_id
        self.origin = origin
        self.destination = destination
        self.date = date
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.price = price

    def __repr__(self):
        return f"Flight({self.airline} {self.flight_id}, {self.origin}->{self.destination}, ${self.price})"


class Booking:
    """Represents a confirmed booking."""

    _counter = 0

    def __init__(self, user, flight, passenger_name):
        Booking._counter += 1
        self.booking_id = f"TS{Booking._counter:04d}"
        self.user = user
        self.flight = flight
        self.passenger_name = passenger_name
        self.booked_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.status = "Confirmed"

    def __repr__(self):
        return f"Booking({self.booking_id}, {self.flight.origin}->{self.flight.destination})"


def generate_flights(origin, destination, date):
    """Generate random flight options between two cities on a given date."""
    flights = []
    num_flights = random.randint(5, 10)
    base_price = random.randint(80, 350)

    for i in range(num_flights):
        airline = random.choice(AIRLINES)
        flight_num = random.randint(100, 9999)
        dep_hour = random.randint(5, 22)
        dep_min = random.choice([0, 15, 30, 45])
        duration_h = random.randint(1, 5)
        duration_m = random.choice([0, 15, 30, 45])

        arr_hour = (dep_hour + duration_h + (dep_min + duration_m) // 60) % 24
        arr_min = (dep_min + duration_m) % 60

        price = base_price + random.randint(-50, 100)
        if price < 49:
            price = 49

        flights.append(Flight(
            airline=airline,
            flight_id=str(flight_num),
            origin=origin,
            destination=destination,
            date=date,
            departure_time=f"{dep_hour:02d}:{dep_min:02d}",
            arrival_time=f"{arr_hour:02d}:{arr_min:02d}",
            price=price,
        ))

    return flights
