from decimal import Decimal
import logging
import pandas as pd

from app.calculator_config import CalculatorConfig
from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento
from app.exceptions import ValidationError, OperationError
from app.history import HistoryObserver
from app.input_validators import InputValidator
from app.operations import OperationFactory
from app.logger import setup_logger

class Calculator:
    def __init__(self):
        self.config = CalculatorConfig()
        self.config.log_dir.mkdir(parents=True, exist_ok=True)
        self.config.history_dir.mkdir(parents=True, exist_ok=True)

        setup_logger(self.config.log_dir / "calculator.log")

        self.history = []
        self.undo_stack = []
        self.redo_stack = []
        self.observers = []

    def add_observer(self, observer: HistoryObserver) -> None:
        self.observers.append(observer)

    def notify_observers(self, calculation: Calculation) -> None:
        for observer in self.observers:
            observer.update(calculation)
    
    def calculate(self, operation_name: str, a: str, b: str) -> Decimal:
        try:
            operand1 = InputValidator.validate_number(a, self.config.max_input_value)
            operand2 = InputValidator.validate_number(b, self.config.max_input_value)

            operation = OperationFactory.get_operation(operation_name)
            result = operation.execute(operand1, operand2)

            self.undo_stack.append(CalculatorMemento(self.history.copy()))
            self.redo_stack.clear()

            calculation = Calculation(
                operation=operation, 
                operand1=operand1, 
                operand2=operand2, 
                result=result
            )

            self.history.append(calculation)

            if len(self.history) > self.config.max_history_size:
                self.history.pop(0)

            self.notify_observers(calculation)

            return result
        
        except ValidationError:
            raise
        except Exception as exc:
            logging.error(f"Error during calculation: {exc}")
            raise OperationError(f"An error occurred during the operation: {exc}") from exc
        
    def get_history(self):
        return self.history

    def clear_history(self)-> None:
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.history.clear()
        self.redo_stack.clear()

    def undo(self) -> bool:
        if not self.undo_stack:
            return False

        memento = self.undo_stack.pop()
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()
        return True
    
    def redo(self) -> bool:
        if not self.redo_stack:
            return False

        memento = self.redo_stack.pop()
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()
        return True
    
    def save_history(self) -> None:
        try:
            data = [calc.to_dict() for calc in self.history]
            df = pd.DataFrame(
                data, 
                columns=["operation", "operand1", "operand2", "result", "timestamp"]
            )
            df.to_csv(
                self.config.history_dir / "calculator_history.csv", 
                index=False, 
                encoding=self.config.default_encoding
            )
            logging.info("History saved successfully.")
        except Exception as exc:
            raise OperationError(f"Failed to save history: {exc}") from exc
        
    def load_history(self) -> None:
        try:
            history_file = self.config.history_dir / "calculator_history.csv"
            if not history_file.exists():
                self.history = []
                return

            df = pd.read_csv(
                history_file, 
                encoding=self.config.default_encoding
            )
            self.history = [
                Calculation.from_dict(row.to_dict())
                for _, row in df.iterrows()
            ]
            logging.info("History loaded successfully.")
        except Exception as exc:
            raise OperationError(f"Failed to load history: {exc}") from exc