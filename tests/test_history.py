from decimal import Decimal
from unittest.mock import Mock, patch

from app.calculation import Calculation
from app.history import LoggingObserver, AutoSaveObserver


def test_logging_observer_update():
    calculation = Calculation("Addition", Decimal("2"), Decimal("3"), Decimal("5"))
    observer = LoggingObserver()

    with patch("app.history.logging.info") as mock_info:
        observer.update(calculation)

    mock_info.assert_called_once()


def test_auto_save_observer_when_enabled():
    calculator = Mock()
    calculator.config.auto_save = True

    observer = AutoSaveObserver(calculator)
    calculation = Calculation("Addition", Decimal("2"), Decimal("3"), Decimal("5"))

    observer.update(calculation)

    calculator.save_history.assert_called_once()


def test_auto_save_observer_when_disabled():
    calculator = Mock()
    calculator.config.auto_save = False

    observer = AutoSaveObserver(calculator)
    calculation = Calculation("Addition", Decimal("2"), Decimal("3"), Decimal("5"))

    observer.update(calculation)

    calculator.save_history.assert_not_called()