from .errors import ValidationError

VALID_STATUSES = ("PLANNED", "ONGOING", "COMPLETED", "CANCELLED")

def validate_status(data):
    if not isinstance (data,dict):
        raise ValidationError ("Input data must be in JSON format")
    
    if "status" not in data:
        raise ValidationError("Missing required field: status")

    status = data["status"]
    if not isinstance(status, str) or not status.strip():
        raise ValidationError("Status must be a non-empty string.")

    status = status.strip()
    if status not in VALID_STATUSES:
        raise ValidationError(
            f"Status must be one of: {', '.join(VALID_STATUSES)}."
        )

    return status