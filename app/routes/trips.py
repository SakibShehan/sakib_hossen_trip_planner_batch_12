from flask import Blueprint, jsonify, request

from ..services import trip_service

trips_bp = Blueprint("trips", __name__)


@trips_bp.post("/api/v1/trips")
def create_trip():
    data = request.get_json(silent=True)
    trip = trip_service.create_trip(data)
    return trip.to_dict(), 201


@trips_bp.get("/api/v1/trips")
def get_trips():
    trips = trip_service.get_all_trips()
    return jsonify([trip.to_dict() for trip in trips]), 200


@trips_bp.get("/api/v1/trips/<int:trip_id>")
def get_trip(trip_id):
    trip = trip_service.get_trip(trip_id)
    return trip.to_dict(), 200


@trips_bp.put("/api/v1/trips/<int:trip_id>")
def update_trip(trip_id):
    data = request.get_json(silent=True)
    trip = trip_service.update_trip(trip_id, data)
    return trip.to_dict(), 200


@trips_bp.delete("/api/v1/trips/<int:trip_id>")
def remove_trip(trip_id):
    trip_service.delete_trip(trip_id)
    return {"message": "Trip deleted successfully."}, 200


@trips_bp.patch("/api/v1/trips/<int:trip_id>/status")
def change_trip_status(trip_id):
    data = request.get_json()
    trip = trip_service.change_trip_status(trip_id, data)
    return trip.to_dict(), 200