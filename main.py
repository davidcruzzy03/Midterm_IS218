from app.calculator import Calculator

def get_numbers():
    a = input("Enter first number: ")
    b = input("Enter second number: ")
    return a, b

def main():
    calculator = Calculator()

    print("Welcome to the Command-Line Calculator!")
    print("Type 'help' for commands.")

    while True:
        command = input("Enter command: ").strip().lower()

        if command == "exit":
            print("Exiting the calculator. Goodbye!")
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
                print(f"Result: {result}")
            except Exception as e:
                print(f"Error: {e}")

        elif command == "history":
            if not calculator.history:
                print("No history available.")
            else:
                print("\nCalculation History:")
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
            print("History cleared.")

        elif command == "undo":
            calculator.undo()
            print("Undo completed.")

        elif command == "redo":
            calculator.redo()
            print("Redo completed.")

        elif command == "save":
            calculator.save_history()
            print("History saved.")

        elif command == "load":
            calculator.load_history()
            print("History loaded.")

        else:
            print("Unknown command. Type 'help' for a list of commands.")     

if __name__ == "__main__":
    main()