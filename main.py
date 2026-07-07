from colorama import Fore, Style, init
from app.calculator import Calculator

def get_numbers():
    a = input("Enter first number: ")
    b = input("Enter second number: ")
    return a, b

def main():
    calculator = Calculator()

    print(Fore.CYAN + "Welcome to the Command-Line Calculator!")
    print(Fore.YELLOW + "Type 'help' for commands.")

    while True:
        command = input("Enter command: ").strip().lower()

        if command == "exit":
            print(Fore.MAGENTA + "Exiting the calculator. Goodbye!")
            break

        elif command == "help":
            print("""
                  Commands:
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
                  exit
                  """)
        

        elif command in [
            "add", 
            "subtract", 
            "multiply", 
            "divide", 
            "power", 
            "root",
            "modulus", 
            "int_divide", 
            "percent", 
            "abs_diff"
        ]:
            try:
                a, b = get_numbers()
                result = calculator.calculate(command, str(a), str(b))
                print(Fore.GREEN + f"Result: {result}")
            except Exception as e:
                print(Fore.RED + f"Error: {e}")

        elif command == "history":
            if not calculator.history:
                print("No history available.")
            else:
                print(Fore.BLUE + "\nCalculation History:")
                for index, calculation in enumerate(calculator.history, start=1):
                    operation_name = calculation.operation

                    if not isinstance(operation_name, str):
                        operation_name = calculation.operation.__class__.__name__

                    print(
                        f"{index}. {operation_name}: "
                        f"{calculation.operand1} and {calculation.operand2} = {calculation.result}"
                    )

        elif command == "clear":
            calculator.clear_history()
            print(Fore.YELLOW + "History cleared.")

        elif command == "undo":
            calculator.undo()
            print(Fore.YELLOW + "Undo completed.")

        elif command == "redo":
            calculator.redo()
            print(Fore.YELLOW + "Redo completed.")

        elif command == "save":
            calculator.save_history()
            print(Fore.GREEN + "History saved.")

        elif command == "load":
            calculator.load_history()
            print(Fore.GREEN + "History loaded.")

        else:
            print(Fore.RED + "Unknown command. Type 'help' for a list of commands.")     

if __name__ == "__main__":
    main()