from ..models.trip import Trip
from ..models.trip_traveler import trip_travelers


def find_overlapping_trip(traveler, start_date, end_date, exclude_trip_id):
 
    return (
        Trip.query
        .join(trip_travelers, trip_travelers.c.trip_id == Trip.id)
        .filter(
            trip_travelers.c.traveler_id == traveler.id,
            Trip.id != exclude_trip_id,
            Trip.status != "CANCELLED",
            Trip.start_date <= end_date,
            Trip.end_date >= start_date,
        )
        .first()
    )