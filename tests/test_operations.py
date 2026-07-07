import pytest
from app.calculator import Calculator

@pytest.fixture
def calculator():
    return Calculator()

@pytest.mark.parametrize(
    "operation, a, b, expected",
    [
        ("add", "5", "3", 8),
        ("subtract", "5", "3", 2),
        ("multiply", "5", "3", 15),
        ("divide", "6", "3", 2),
        ("power", "2", "3", 8),
        ("root", "27", "3", 3),
        ("modulus", "10", "3", 1),
        ("int_divide", "10", "3", 3),
        ("percent", "50", "200", 25),
        ("abs_diff", "5", "3", 2),
    ]
)
def test_calculator_operations(calculator, operation, a, b, expected):
    result = calculator.calculate(operation, a, b)
    assert float(result) == expected

def test_divide_by_zero(calculator):
    with pytest.raises(Exception):
        calculator.calculate("divide", "10", "0")

def test_invalid_operation(calculator):
    with pytest.raises(Exception):
        calculator.calculate("invalid_operation", "2", "2")