from flask import Blueprint, request, jsonify

from ..services import traveler_service

travelers_bp = Blueprint("travelers", __name__)


@travelers_bp.post("/api/v1/trips/<int:trip_id>/travelers")
def add_traveler(trip_id):
    data = request.get_json(force=True, silent=True)
    traveler = traveler_service.add_traveler(trip_id, data)
    return {**traveler.to_dict(), "trip_id": trip_id}, 201

@travelers_bp.delete("/api/v1/trips/<int:trip_id>/travelers/<int:traveler_id>")
def remove_traveler(trip_id, traveler_id):
    traveler_service.remove_traveler(trip_id, traveler_id)
    return {"message": "Traveler removed from the trip successfully."}, 200

#get all travelers just for my use 
@travelers_bp.get("/api/v1/trips/<int:trip_id>/travelers")
def get_all_travelers(trip_id):
    travelers = traveler_service.get_all_travelers(trip_id)
    return jsonify([traveler.to_dict() for traveler in travelers]), 200