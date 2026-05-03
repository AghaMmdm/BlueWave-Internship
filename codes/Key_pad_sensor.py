from machine import Pin
import time

# Define row pins as input
rows = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in ["X22", "X21", "X20", "X19"]]

# Define column pins as output
cols = [Pin(i, Pin.OUT) for i in ["X4", "X3", "X2", "X1"]]

# Keypad layout (transposed)
keys = [
    ['1', '4', '7', '*'],
    ['2', '5', '8', '0'],
    ['3', '6', '9', '#'],
    ['A', 'B', 'C', 'D']
]

# Define valid numbers and operators
nums = ['1','2','3','4','5','6','7','8','9','0']
ops = ['A','B','C','D']  # A:+ , B:- , C:* , D:/

def scan():
    """Scan keypad and return pressed key"""
    for j, col in enumerate(cols):
        col.value(1)
        for i, row in enumerate(rows):
            if row.value() == 1:
                time.sleep(0.2)  # debounce
                return keys[i][j]
        col.value(0)
    return None

# Initialize variables
num1 = None
num2 = None
operation = None
state = "num1"  # states: num1 → op → num2

print("Calculator Ready")

while True:
    key = scan()

    if key is None:
        continue

    print("Pressed:", key)

    # Clear everything
    if key == '*':
        num1 = None
        num2 = None
        operation = None
        state = "num1"
        print("Cleared")
        continue

    # Build first number
    if state == "num1":
        if key in nums:
            if num1 is None:
                num1 = int(key)
            else:
                num1 = num1 * 10 + int(key)

        elif key in ops and num1 is not None:
            operation = key
            state = "num2"
            print("num1:", num1)

    # Build second number
    elif state == "num2":
        if key in nums:
            if num2 is None:
                num2 = int(key)
            else:
                num2 = num2 * 10 + int(key)

        # Calculate result
        elif key == '#' and num2 is not None:
            print("num2:", num2)

            if operation == "A":
                result = num1 + num2
            elif operation == "B":
                result = num1 - num2
            elif operation == "C":
                result = num1 * num2
            elif operation == "D":
                if num2 != 0:
                    result = num1 / num2
                else:
                    print("Error: Division by zero")
                    continue

            print("Result:", result)

            # Reset for next calculation
            num1 = result
            num2 = None
            operation = None
            state = "num1"