from .models import Trip
from . import db
from datetime import datetime
from .validation import validate_trip, NotFoundError

def create_trip(data):
    clean_data = validate_trip(data)
    trip = Trip(**clean_data)
    db.session.add(trip)
    db.session.commit()
    return trip

def get_all_trips():
    return Trip.query.order_by(Trip.id).all()

def get_trip(trip_id):
    trip = db.session.get(Trip, trip_id)
    if trip is None:
        raise NotFoundError("Trip not found.")
    return trip