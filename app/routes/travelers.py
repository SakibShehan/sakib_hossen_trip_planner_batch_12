from flask import Blueprint, request

from ..services import traveler_service

travelers_bp = Blueprint("travelers", __name__)


@travelers_bp.post("/api/v1/trips/<int:trip_id>/travelers")
def add_traveler(trip_id):
    data = request.get_json(force=True, silent=True)
    traveler = traveler_service.add_traveler(trip_id, data)
    return {**traveler.to_dict(), "trip_id": trip_id}, 201