from flask import Blueprint, request
from . import services
from .validation import ValidationError

bp = Blueprint("main", __name__)


@bp.get("/health")
def health():
    return {"status": "ok"}

@bp.post("/api/v1/trips")
def create_trip():
    data = request.get_json()

    try:
        trip = services.create_trip(data)
    except ValidationError as error:
        return {"error": "VALIDATION_ERROR", "message": error.message}, 400
    
    return trip.to_dict(), 201