from decimal import Decimal, InvalidOperation
from app.exceptions import ValidationError

class InputValidator:
    @staticmethod
    def validate_number(value: str, max_value: Decimal) -> Decimal:
        try:
            number = Decimal(value)
        except InvalidOperation as exc:
            raise ValidationError(f"'{value}' is not a valid number.") from exc

        if abs(number) > max_value:
            raise ValidationError(
                f"Input {number} is too large. Maximum allowed is {max_value}."
            )

        return number
    