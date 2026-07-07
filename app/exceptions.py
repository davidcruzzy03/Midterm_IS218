class CalculatorError(Exception):
    """Base class for calculator exceptions."""
    pass

class ValidationError(CalculatorError):
    """Exception raised for validation errors."""
    pass

class OperationError(CalculatorError):
    """Exception raised for operation errors."""
    pass

class ConfigurationError(CalculatorError):
    """Exception raised for configuration errors."""
    pass

class HistoryError(CalculatorError):
    """Exception raised for history-related errors."""
    pass
