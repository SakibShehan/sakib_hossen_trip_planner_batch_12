from flask import Blueprint

from ..services import summary_service

summary_bp = Blueprint("summary", __name__)


@summary_bp.get("/api/v1/trips/<int:trip_id>/summary")
def get_trip_summary(trip_id):
    summary = summary_service.get_trip_summary(trip_id)
    return summary, 200