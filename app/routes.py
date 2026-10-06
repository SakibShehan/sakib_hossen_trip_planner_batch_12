from flask import Blueprint, request
from . import services

bp = Blueprint("main", __name__)


@bp.get("/health")
def health():
    return {"status": "ok"}

@bp.post("/api/v1/trips")
def create_trip():
    data = request.get_json()
    trip= services.create_trip(data)
    return trip.to_dict(), 201