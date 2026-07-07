# Enchanced Calculator Command-Line Application

## Project Description

This project is an enchanced command-line calculator built with Pyhton. It supports multiple arithmetic operations, 
input validation, error handling, calculation history, undo/redo functionality, logging, 
and CSV-based history persistence using pandas.

The application uses object-oriented programming and design patterns such as Factory, Memento, and Observer.

## Features

- Addition
- Subtraction
- Multiplication
- Division
- Power
- Root
- Modulus
- Integer division
- Percentage calculation
- Absolute difference
- Calculation history
- Undo and Redo
- Save and load history
- Logging
- Environment-based configuration
- Unit testing with pytest
- GitHub Actions CI workflow

## insallation

Clone the repoistory:

'''bash
git clone git@github.com:davidcruzzy03/Midterm_IS218.git
cd Midterm_IS218

```bash
git clone git@github.com:davidcruzzy03/Midterm_IS218.git
cd Midterm_IS218
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

```env
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

Usage Guide:

```bash
python3 main.py
```

Available Commands:

```
add
subtract
multiply
divide
power
root
modulus
int_divide
percent
abs_diff
history
undo
redo
clear
save
load
help
exit
```

Testing Instruction:

```bash
pytest
```

```bash
pytest --cov=app --cov-fail-under=90
```