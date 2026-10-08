from .. import db
from ..models.trip import Trip
from ..validators.errors import ConflictError, NotFoundError
from ..validators.trip_validator import validate_trip
from ..validators.status_validator import validate_status
from .overlap_service import find_overlapping_trip


ALLOWED_TRANSITIONS = {
    "PLANNED": ("ONGOING", "CANCELLED"),
    "ONGOING": ("COMPLETED", "CANCELLED"),
    "COMPLETED": (),
    "CANCELLED": (),
}

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

    # max travelers must not go below the current traveler count
    current_traveler_count = len(trip.travelers)
    if clean_data["max_travelers"] < current_traveler_count:
        raise ConflictError(
            "CAPACITY_BELOW_TRAVELER_COUNT",
            f"max_travelers cannot be less than the current traveler count ({current_traveler_count}).",
        )

    # new dates must not overlap another active trip of any traveler 
    dates_changed = (
        clean_data["start_date"] != trip.start_date or clean_data["end_date"] != trip.end_date
    )
    if dates_changed:
        for traveler in trip.travelers:
            overlapping_trip = find_overlapping_trip(
                traveler, clean_data["start_date"], clean_data["end_date"], trip.id
            )
            if overlapping_trip is not None:
                raise ConflictError(
                    "TRAVELER_TRIP_OVERLAP",
                    f"The new dates overlap trip {overlapping_trip.id} for traveler {traveler.email}.",
                )

    trip.destination = clean_data["destination"]
    trip.start_date = clean_data["start_date"]
    trip.end_date = clean_data["end_date"]
    trip.budget = clean_data["budget"]
    trip.max_travelers = clean_data["max_travelers"]

    db.session.commit()
    return trip



def change_trip_status(trip_id, data):
  
    trip = get_trip(trip_id)

    # validate status
    new_status = validate_status(data)

    # valid transiton cjeck from defined transitions
    if new_status not in ALLOWED_TRANSITIONS[trip.status]:
        raise ConflictError(
            "INVALID_STATUS_TRANSITION",
            f"A trip cannot change from {trip.status} to {new_status}.",
        )

    trip.status = new_status
    db.session.commit()
    return trip