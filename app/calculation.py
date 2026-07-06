from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict


@dataclass
class Calculation:
    operation: str
    operand1: Decimal
    operand2: Decimal
    result: Decimal
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation": self.operation,
            "operand1": str(self.operand1),
            "operand2": str(self.operand2),
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Calculation":
        return Calculation(
            operation=data["operation"],
            operand1=Decimal(data["operand1"]),
            operand2=Decimal(data["operand2"]),
            result=Decimal(data["result"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )

    def __str__(self) -> str:
        return f"{self.operation}({self.operand1}, {self.operand2}) = {self.result}"