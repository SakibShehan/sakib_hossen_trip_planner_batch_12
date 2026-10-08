from datetime import datetime

from .errors import ValidationError
from .money_validator import validate_money

MAX_DESTINATION_LENGTH = 100
MAX_BUDGET = 1_000_000_000
MAX_TRAVELERS_LIMIT = 10_000

REQUIRED_FIELDS = ["destination", "start_date", "end_date", "budget", "max_travelers"]


def parse_date(value, field):
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a string in 'YYYY-MM-DD' format.")
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError(f"{field} must be in 'YYYY-MM-DD' format.")


def validate_trip(data):

    # input data type check
    if not isinstance(data, dict):
        raise ValidationError("Input data must be a JSON object.")

    # check any field is absent or not
    for field in REQUIRED_FIELDS:
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")

    # check each field from here
    destination = data["destination"]
    if not isinstance(destination, str) or not destination.strip():
        raise ValidationError("Destination must be a non-empty string.")
    destination = destination.strip()
    if len(destination) > MAX_DESTINATION_LENGTH:
        raise ValidationError(f"Destination must be at most {MAX_DESTINATION_LENGTH} characters.")

    budget = validate_money(data["budget"], "Budget", MAX_BUDGET)

    max_travelers = data["max_travelers"]
    if isinstance(max_travelers, bool) or not isinstance(max_travelers, int) or max_travelers <= 0:
        raise ValidationError("Max travelers must be a positive integer.")
    if max_travelers > MAX_TRAVELERS_LIMIT:
        raise ValidationError(f"Max travelers must not exceed {MAX_TRAVELERS_LIMIT}.")

    start_date = parse_date(data["start_date"], "start_date")
    end_date = parse_date(data["end_date"], "end_date")

    if start_date >= end_date:
        raise ValidationError("Start date must be before end date.")

    return {
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "max_travelers": max_travelers,
    }