import re

from .errors import ValidationError

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 254


def validate_traveler(data):
    if not isinstance(data, dict):
        raise ValidationError("Input data must be a JSON object.")

    for field in ("name", "email"):
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")

    name = data["name"]
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Name must be a non-empty string.")
    name = name.strip()
    if len(name) > MAX_NAME_LENGTH:
        raise ValidationError(f"Name must be at most {MAX_NAME_LENGTH} characters.")

    email = data["email"]
    if not isinstance(email, str) or not email.strip():
        raise ValidationError("Email must be a non-empty string.")
    email = email.strip().lower()
    if len(email) > MAX_EMAIL_LENGTH or not EMAIL_PATTERN.match(email):
        raise ValidationError("Email must be a valid email address.")

    return {"name": name, "email": email}