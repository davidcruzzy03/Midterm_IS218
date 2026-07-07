import pytest

from app.input_validators import InputValidator
from app.exceptions import ValidationError

def test_validate_number_invalid_input():
        with pytest.raises(ValidationError):
                InputValidator.validate_number("abc", 100)

def test_validate_number_too_large():
        with pytest.raises(ValidationError):
                InputValidator.validate_number("101", 100)
    
def test_validate_number_valid():
        result = InputValidator.validate_number("50", 100)
        assert result == 50
