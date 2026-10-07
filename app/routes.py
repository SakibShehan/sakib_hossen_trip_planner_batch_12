from flask import Blueprint, request, jsonify
from . import services
from .validation import ValidationError,register_error_handlers

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

@bp.get("/api/v1/trips/<int:trip_id>")
def get_trip(trip_id):
    trip = services.get_trip(trip_id)
    return trip.to_dict(), 200

@bp.delete("/api/v1/trips/<int:trip_id>")
def remove_trip(trip_id):
    services.delete_trip(trip_id)
    return {"message": "Trip deleted successfully."}, 200

@bp.put("/api/v1/trips/<int:trip_id>")
def update_trip(trip_id):
    data = request.get_json()
    trip= services.update_trip(trip_id,data)
    return trip.to_dict(), 200