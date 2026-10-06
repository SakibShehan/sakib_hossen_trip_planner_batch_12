from flask import Blueprint, request, jsonify
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

@bp.get("/api/v1/trips")
def get_trips():
    trips = services.get_all_trips()
    return jsonify([trip.to_dict() for trip in trips]), 200