import math

from .errors import ValidationError

MAX_TITLE_LENGTH = 100
MAX_AMOUNT = 1_000_000_000


def validate_expense(data):
    if not isinstance(data, dict):
        raise ValidationError("Input data must be a JSON object.")

    for field in ("title", "amount"):
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")

    title = data["title"]
    if not isinstance(title, str) or not title.strip():
        raise ValidationError("Title must be a non-empty string.")
    title = title.strip()
    if len(title) > MAX_TITLE_LENGTH:
        raise ValidationError(f"Title must be at most {MAX_TITLE_LENGTH} characters.")

    amount = data["amount"]
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValidationError("Amount must be a number.")
    if not math.isfinite(amount) or amount <= 0:
        raise ValidationError("Amount must be greater than zero.")
    if amount > MAX_AMOUNT:
        raise ValidationError(f"Amount must not exceed {MAX_AMOUNT}.")
    # money has at most 2 decimal points
    if abs(amount * 100 - round(amount * 100)) > 1e-6:
        raise ValidationError("Amount must have at most 2 decimal places.")

    return {"title": title, "amount": round(amount, 2)}