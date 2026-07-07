import pytest
from decimal import Decimal
from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError

from unittest.mock import Mock, patch
from app.history import LoggingObserver

@pytest.fixture
def calculator(tmp_path):
    calc = Calculator()
    calc.config.history_dir = tmp_path
    calc.config.default_encoding = "utf-8"
    return calc

def test_calculator_initialization(calculator):
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.observers == []

@pytest.mark.parametrize(
    "operation, a, b, expected",
    [
        ("add", "5", "3", Decimal("8")),
        ("subtract", "5", "3", Decimal("2")),
        ("multiply", "5", "3", Decimal("15")),
        ("divide", "6", "3", Decimal("2")),
        ("power", "2", "3", Decimal("8")),
        ("root", "27", "3", Decimal("3")),
        ("modulus", "10", "3", Decimal("1")),
        ("int_divide", "10", "3", Decimal("3")),
        ("percent", "50", "200", Decimal("25")),
        ("abs_diff", "5", "3", Decimal("2")),
    ]
)
def test_calculator_operations(calculator, operation, a, b, expected):
    result = calculator.calculate(operation, a, b)
    assert result == expected

def test_power(calculator):
    result = calculator.calculate("power", "2", "3")
    assert result == Decimal("8")

def test_root(calculator):
    result = calculator.calculate("root", "27", "3")
    assert float(result) == 3.0

def test_invalid_operation(calculator):
    with pytest.raises(OperationError):
        calculator.calculate("invalid_operation", "2", "2")

def test_divide_by_zero(calculator):
    with pytest.raises(ValidationError):
        calculator.calculate("divide", "10", "0")

def test_percent_by_zero(calculator):
    with pytest.raises(ValidationError):
        calculator.calculate("percent", "50", "0")

def test_root_negative_number(calculator):
    with pytest.raises(ValidationError):
        calculator.calculate("root", "-27", "3")

def test_root_zero_degree(calculator):
    with pytest.raises(ValidationError):
        calculator.calculate("root", "27", "0")

def test_history_added_after_calculation(calculator):
    calculator.calculate("add", "2", "2")
    assert len(calculator.history) == 1
    assert calculator.history[0].operand1 == Decimal("2")
    assert calculator.history[0].operand2 == Decimal("2")
    assert calculator.history[0].result == Decimal("4")

def test_get_history(calculator):
    calculator.calculate("add", "2", "2")
    history = calculator.get_history()
    assert len(history) == 1

def test_clear_history(calculator):
    calculator.calculate("add", "2", "2")
    calculator.clear_history()
    assert calculator.history == []
    assert calculator.redo_stack == []

def test_undo_redo(calculator):
    calculator.calculate("add", "2", "2")
    result = calculator.undo()
    assert result is True
    assert calculator.history == []

def test_undo_empty_returns_false(calculator):
    result = calculator.undo()
    assert result is False

def test_redo(calculator):
    calculator.calculate("add", "2", "2")
    calculator.undo()
    result = calculator.redo()
    assert result is True
    assert len(calculator.history) == 1
  
def test_redo_empty_returns_false(calculator):
    result = calculator.redo()
    assert result is False

def test_save_history(calculator):
    calculator.calculate("add", "2", "2")
    calculator.save_history()
    history_file = calculator.config.history_dir / "calculator_history.csv"
    assert history_file.exists()

def test_load_history(calculator):
    calculator.calculate("add", "2", "2")
    calculator.save_history()
    calculator.clear_history()
    assert calculator.history == []
    calculator.load_history()
    assert len(calculator.history) == 1
    assert calculator.history[0].operand1 == Decimal("2")
    assert calculator.history[0].operand2 == Decimal("2")
    assert calculator.history[0].result == Decimal("4")

def test_load_history_no_file(calculator):
    calculator.load_history()
    assert calculator.history == []

def test_max_history_size(calculator):
    calculator.config.max_history_size = 1
    calculator.calculate("add", "1", "1")
    calculator.calculate("add", "2", "2")
    assert len(calculator.history) == 1
    assert calculator.history[0].result == Decimal("4")

def test_add_observer_and_notify(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)

    with patch.object(observer, "update") as mock_update:
        calculator.calculate("add", "2", "2")

    mock_update.assert_called_once()

def test_notify_multiple_observers(calculator):
    observer_one = Mock()
    observer_two = Mock()

    calculator.add_observer(observer_one)
    calculator.add_observer(observer_two)

    calculator.calculate("add", "2", "2")

    observer_one.update.assert_called_once()
    observer_two.update.assert_called_once()

def test_save_history_error(calculator):
    calculator.calculate("add", "2", "2")

    with patch("app.calculator.pd.DataFrame.to_csv", side_effect=Exception("save failed")):
        with pytest.raises(OperationError):
            calculator.save_history()

def test_load_history_error(calculator):
    history_file = calculator.config.history_dir / "calculator_history.csv"
    history_file.write_text("operation,operand1,operand2,result,timestamp\nbad,bad,bad,bad,bad")

    with pytest.raises(OperationError):
        calculator.load_history()