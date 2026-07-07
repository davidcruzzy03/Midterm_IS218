from decimal import Decimal
import pytest

from app.exceptions import ValidationError
from app.operations import OperationFactory, Operation

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
def test_calculator_operations(operation, a, b, expected):
    operation_object = OperationFactory.get_operation(operation)
    result = operation_object.execute(Decimal(a), Decimal(b))
    assert float(result) == expected

def test_get_operation_case_insensitive():
    operation = OperationFactory.get_operation("ADD")
    assert operation is OperationFactory.operations["add"]

def test_invalid_operation():
    with pytest.raises(ValueError):
        OperationFactory.get_operation("invalid_operation")

def test_register_invalid_operation_type():
    with pytest.raises(TypeError):
        OperationFactory.register_operation("bad", "not an operation instance")

def test_base_operation_validate():
    class TestOperation(Operation):
        def execute(self, a, b):
            return Decimal("0")

    operation = TestOperation()
    assert operation.validate(Decimal("5"), Decimal("3")) is None

def test_divide_by_zero():
    operation = OperationFactory.get_operation("divide")

    with pytest.raises(ValidationError):
        operation.execute(Decimal("10"), Decimal("0"))


def test_power_negative_exponent():
    operation = OperationFactory.get_operation("power")

    with pytest.raises(ValidationError):
        operation.execute(Decimal("2"), Decimal("-1"))


def test_root_negative_number():
    operation = OperationFactory.get_operation("root")

    with pytest.raises(ValidationError):
        operation.execute(Decimal("-27"), Decimal("3"))


def test_root_zero_degree():
    operation = OperationFactory.get_operation("root")

    with pytest.raises(ValidationError):
        operation.execute(Decimal("27"), Decimal("0"))


def test_modulus_by_zero():
    operation = OperationFactory.get_operation("modulus")

    with pytest.raises(ValidationError):
        operation.execute(Decimal("10"), Decimal("0"))


def test_integer_division_by_zero():
    operation = OperationFactory.get_operation("int_divide")

    with pytest.raises(ValidationError):
        operation.execute(Decimal("10"), Decimal("0"))


def test_percentage_by_zero():
    operation = OperationFactory.get_operation("percent")

    with pytest.raises(ValidationError):
        operation.execute(Decimal("10"), Decimal("0")) 

def test_operation_abstract_execute():
    with pytest.raises(TypeError):
        Operation()

def test_register_valid_operation():
    class CustomOperation(Operation):
        def execute(self, a, b):
            return Decimal("100")
    operation = CustomOperation()
    OperationFactory.register_operation("custom", operation)
    assert OperationFactory.get_operation("custom") is operation
    assert OperationFactory.get_operation("custom").execute(Decimal("1"), Decimal("2")) == Decimal("100")