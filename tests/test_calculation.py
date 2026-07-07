from datetime import datetime
from decimal import Decimal

from app.calculation import Calculation

def test_calculation_creation():
    calculation = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3"),
        result=Decimal("5"),
    )
    assert calculation.operation == "Addition"
    assert calculation.operand1 == Decimal("2")
    assert calculation.operand2 == Decimal("3")
    assert calculation.result == Decimal("5")
    assert isinstance(calculation.timestamp, datetime)

def test_calculation_to_dict():
    timestamp = datetime.now()
    calculation = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3"),
        result=Decimal("5"),
        timestamp=timestamp,
    )
    data = calculation.to_dict()
    assert data["operation"] == "Addition"
    assert data["operand1"] == "2"
    assert data["operand2"] == "3"
    assert data["result"] == "5"
    assert data["timestamp"] == timestamp.isoformat()

def test_calculation_from_dict():
    timestamp = datetime.now()
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": timestamp.isoformat(),
    }
    calculation = Calculation.from_dict(data)
    assert calculation.operation == "Addition"
    assert calculation.operand1 == Decimal("2")
    assert calculation.operand2 == Decimal("3")
    assert calculation.result == Decimal("5")
    assert calculation.timestamp == timestamp

def test_calculation_str():
    calculation = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3"),
        result=Decimal("5"),
    )
    assert str(calculation) == "Addition(2, 3) = 5"

