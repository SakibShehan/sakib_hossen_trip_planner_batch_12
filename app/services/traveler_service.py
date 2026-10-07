from sqlalchemy.exc import IntegrityError

from .. import db
from ..models.trip import Trip
from ..models.traveler import Traveler
from ..models.trip_traveler import trip_travelers
from ..validators.errors import ConflictError, NotFoundError
from ..validators.traveler_validator import validate_traveler
from .trip_service import get_trip



def find_overlapping_trip(traveler, trip):
   #find overlapping trip for a traveler excluding the current trip and cancelled trips
    return (
        Trip.query
        .join(trip_travelers, trip_travelers.c.trip_id == Trip.id)
        .filter(
            trip_travelers.c.traveler_id == traveler.id,
            Trip.id != trip.id,
            Trip.status != "CANCELLED",
            Trip.start_date <= trip.end_date,
            Trip.end_date >= trip.start_date,
        )
        .first()
    )


def add_traveler(trip_id, data):
    # check trip exist or not  
    trip = get_trip(trip_id)

    # check trip status is PLANNED or not  
    if trip.status != "PLANNED":
        raise ConflictError(
            "TRIP_NOT_OPEN_FOR_TRAVELERS",
            f"Travelers can only be added to a PLANNED trip. This trip is {trip.status}.",
        )

    # validate imput data
    clean_data = validate_traveler(data)

    # check if traveler already exists in the database
    traveler = Traveler.query.filter_by(email=clean_data["email"]).first()

    # duplicate trvler check in same trip 
    if traveler is not None and traveler in trip.travelers:
        raise ConflictError(
            "DUPLICATE_TRAVELER",
            "This traveler has already joined this trip.",
        )

    # check a trips capacity is not full
    if len(trip.travelers) >= trip.max_travelers:
        raise ConflictError(
            "TRIP_FULL",
            "The trip has reached its maximum traveler capacity.",
        )

    # check overlapping dates for the same traveler in other trips
    if traveler is not None:
        overlapping_trip = find_overlapping_trip(traveler, trip)
        if overlapping_trip is not None:
            raise ConflictError(
                "TRAVELER_TRIP_OVERLAP",
                f"This traveler already has an overlapping trip (trip id {overlapping_trip.id}).",
            )

    # create the traveler if new, then link
    if traveler is None:
        traveler = Traveler(name=clean_data["name"], email=clean_data["email"])
        db.session.add(traveler)

    trip.travelers.append(traveler)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ConflictError(
            "DUPLICATE_TRAVELER",
            "This traveler has already joined this trip.",
        )

    return traveler



def remove_traveler(trip_id, traveler_id):
    # check trip exist or not 
    trip = get_trip(trip_id)

    
    if trip.status != "PLANNED":
        raise ConflictError(
            "TRIP_NOT_OPEN_FOR_TRAVELERS",
            f"Travelers can only be removed from a PLANNED trip. This trip is {trip.status}.",
        )

    # traveler must exist 
    traveler = db.session.get(Traveler, traveler_id)
    if traveler is None:
        raise NotFoundError("Traveler not found.")

    # travler should include in the trip
    if traveler not in trip.travelers:
        raise NotFoundError("This traveler is not part of this trip.")

    # remove travler and commit in db
    trip.travelers.remove(traveler)
    db.session.commit()

#only for personal use to see all travelers in a trip 
def get_all_travelers(trip_id):
    trip = get_trip(trip_id)
    return trip.travelers