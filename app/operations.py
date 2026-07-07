from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict
from app.exceptions import ValidationError

class Operation(ABC):
    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        pass  # pragma: no cover
    def validate(self, a: Decimal, b: Decimal) -> None:
        pass  # pragma: no cover

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
    def validate(self, a: Decimal, b: Decimal) -> None:
        super().validate(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed.")
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return a / b
    
class Power(Operation):
    def validate(self, a: Decimal, b: Decimal) -> None:
        super().validate(a, b)
        if b < 0:
            raise ValidationError("Zero cannot be raised to a negative power.")
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return Decimal(pow(float(a), float(b)))
    
class Root(Operation):
    def validate(self, a: Decimal, b: Decimal) -> None:
        super().validate(a, b)
        if a < 0:
            raise ValidationError("Cannot calculate the root of a negative number.")    
        if b == 0:
            raise ValidationError("Root degree cannot be zero.")
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return Decimal(pow(float(a), float(1) / float(b)))
    
class Modulus(Operation):
    def validate(self, a: Decimal, b: Decimal) -> None:
        super().validate(a, b)
        if b == 0:
            raise ValidationError("Modulus by zero is not allowed.")
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return a % b
    
class IntegerDivision(Operation):
    def validate(self, a: Decimal, b: Decimal) -> None:
        super().validate(a, b)
        if b == 0:
            raise ValidationError("Integer division by zero is not allowed.")
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return a // b
    
class Percentage(Operation):
    def validate(self, a: Decimal, b: Decimal) -> None:
        super().validate(a, b)
        if b == 0:
            raise ValidationError("Percentage denominator cannot be zero.")
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return (a / b) * Decimal("100")
    
class Absolute(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return abs(a-b)

class OperationFactory:
    operations: Dict[str, Operation] = {
        "add": Addition(),
        "subtract": Subtraction(),
        "multiply": Multiplication(),
        "divide": Division(),
        "power": Power(),
        "root": Root(),
        "modulus": Modulus(),
        "int_divide": IntegerDivision(),
        "percent": Percentage(),
        "abs_diff": Absolute()
    }

    @classmethod
    def register_operation(cls, operation_name: str, operation: Operation) -> None:
        if not isinstance(operation, Operation):
            raise TypeError("Operation must be a subclass of Operation.")
        cls.operations[operation_name.lower()] = operation
        
    @classmethod
    def get_operation(cls, operation_name: str) -> Operation:
        operation = cls.operations.get(operation_name.lower())
        if not operation:
            raise ValueError(f"Operation '{operation_name}' is not supported.")
        return operation