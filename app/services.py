from .models import Trip
from . import db
from datetime import datetime


def create_trip(data):
    trip = Trip(
        destination=data["destination"],
        start_date=datetime.strptime(data["start_date"], "%Y-%m-%d").date(),
        end_date=datetime.strptime(data["end_date"], "%Y-%m-%d").date(),
        budget=data["budget"],
        max_travelers=data["max_travelers"],
    )
    db.session.add(trip)
    db.session.commit()
    return trip