from abc import ABC, abstractmethod
import logging
from typing import Any
from app.calculation import Calculation

class HistoryObserver(ABC):
    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        pass  # pragma: no cover
class LoggingObserver(HistoryObserver):
    def update(self, calculation: Calculation) -> None:
        logging.info(
            f"{calculation.operation}: "
            f"{calculation.operand1}, "
            f"{calculation.operand2} = "
            f"{calculation.result}"
        )

class AutoSaveObserver(HistoryObserver):
    def __init__(self, calculator):
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        if self.calculator.config.auto_save:
            self.calculator.save_history()