from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict
from app.exceptions import ValidationError

class Operation(ABC):
    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        pass
    def validate(self, a: Decimal, b: Decimal) -> None:
        pass

class Addition(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return a + b
    
class Subtraction(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return a - b
    
class Multiplication(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return a * b
    
class Division(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed.")
        return a / b