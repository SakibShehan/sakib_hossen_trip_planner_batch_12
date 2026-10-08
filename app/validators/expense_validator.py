from .errors import ValidationError
from .money_validator import validate_money

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

    amount = validate_money(data["amount"], "Amount", MAX_AMOUNT)

    return {"title": title, "amount": amount}