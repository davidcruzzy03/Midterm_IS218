from decimal import Decimal
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

class CalculatorConfig:
    def __init__(self):
        self.log_dir = Path(os.getenv("CALCULATOR_LOG_DIR", "logs"))
        self.history_dir = Path(os.getenv("CALCULATOR_HISTORY_DIR", "history"))
        self.max_history_size = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100"))
        self.auto_save = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"
        self.precision = int(os.getenv("CALCULATOR_PRECISION", "2"))
        self.max_input_value = Decimal(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000"))
        self.default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")
