from .. import db
from ..models.trip import Trip
from ..validators.errors import ConflictError, NotFoundError
from ..validators.trip_validator import validate_trip


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


def delete_trip(trip_id):
    trip = get_trip(trip_id)
    db.session.delete(trip)
    db.session.commit()


def update_trip(trip_id, data):
    trip = get_trip(trip_id)

    if trip.status not in ("PLANNED", "ONGOING"):
        raise ConflictError("TRIP_NOT_EDITABLE", f"A {trip.status} trip cannot be edited.")

    clean_data = validate_trip(data)

    trip.destination = clean_data["destination"]
    trip.start_date = clean_data["start_date"]
    trip.end_date = clean_data["end_date"]
    trip.budget = clean_data["budget"]
    trip.max_travelers = clean_data["max_travelers"]

    db.session.commit()
    return trip

