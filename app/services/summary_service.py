from .trip_service import get_trip


def _to_cents(value):
    return round(value * 100)


def get_trip_summary(trip_id):

    trip = get_trip(trip_id)

    traveler_count = len(trip.travelers)
   
    available_seats = max(0, trip.max_travelers - traveler_count)

    spent_cents = sum(_to_cents(expense.amount) for expense in trip.expenses)
    remaining_cents = _to_cents(trip.budget) - spent_cents

    return {
        "trip_id": trip.id,
        "destination": trip.destination,
        "status": trip.status,
        "budget": trip.budget,
        "max_travelers": trip.max_travelers,
        "traveler_count": traveler_count,
        "available_seats": available_seats,
        "total_expense": spent_cents / 100,
        "remaining_budget": remaining_cents / 100,
    }