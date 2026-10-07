from .. import db
from ..models.expense import Expense
from ..validators.errors import ConflictError
from ..validators.expense_validator import validate_expense
from .trip_service import get_trip


def _to_cents(value):
    #rounding value 
    return round(value * 100)


def add_expense(trip_id, data): 
    trip = get_trip(trip_id)

    # check trips status
    if trip.status not in ("PLANNED", "ONGOING"):
        raise ConflictError(
            "TRIP_NOT_OPEN_FOR_EXPENSES",
            f"Expenses can only be added to a PLANNED or ONGOING trip. This trip is {trip.status}.",
        )

    
    clean_data = validate_expense(data)

    # check total expenses must never exceed the budget 
    spent_cents = sum(_to_cents(expense.amount) for expense in trip.expenses)
    amount_cents = _to_cents(clean_data["amount"])
    budget_cents = _to_cents(trip.budget)

    if spent_cents + amount_cents > budget_cents:
        remaining = (budget_cents - spent_cents) / 100
        raise ConflictError(
            "BUDGET_EXCEEDED",
            f"This expense exceeds the remaining budget of {remaining:.2f}.",
        )

    #save
    expense = Expense(
        trip_id=trip.id,
        title=clean_data["title"],
        amount=clean_data["amount"],
    )
    db.session.add(expense)
    db.session.commit()
    return expense