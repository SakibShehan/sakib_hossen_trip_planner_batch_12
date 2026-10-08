from flask import Blueprint, request

from ..services import expense_service

expenses_bp = Blueprint("expenses", __name__)


@expenses_bp.post("/api/v1/trips/<int:trip_id>/expenses")
def add_expense(trip_id):
    data = request.get_json(force=True, silent=True)
    expense = expense_service.add_expense(trip_id, data)
    return expense.to_dict(), 201