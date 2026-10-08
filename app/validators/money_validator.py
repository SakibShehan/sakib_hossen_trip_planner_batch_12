import math
from decimal import Decimal

from .errors import ValidationError


def validate_money(value, label, max_value):
   
    # booleans rejected
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{label} must be a number.")

    # NaN and Infinity rejected
    if isinstance(value, float) and not math.isfinite(value):
        raise ValidationError(f"{label} must be a finite number.")

    if value <= 0:
        raise ValidationError(f"{label} must be greater than zero.")

    # check upper bound 
    if value > max_value:
        raise ValidationError(f"{label} must not exceed {max_value}.")

    # at most 2 decimal places allowed
    if Decimal(str(value)).as_tuple().exponent < -2:
        raise ValidationError(f"{label} must have at most 2 decimal places.")

    return round(value, 2)