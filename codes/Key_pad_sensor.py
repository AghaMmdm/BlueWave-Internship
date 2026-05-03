from machine import Pin, I2C
import time
import bluelib

# Initialize OLED
i2c = I2C(2)
oled = bluelib.BOled_I2C(128, 32, i2c)
oled.fill(0)
oled.show()

# Keypad setup
rows = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in ["X22", "X21", "X20", "X19"]]
cols = [Pin(i, Pin.OUT) for i in ["X4", "X3", "X2", "X1"]]

keys = [
    ['1', '4', '7', '*'],
    ['2', '5', '8', '0'],
    ['3', '6', '9', '#'],
    ['A', 'B', 'C', 'D']
]

nums = ['1','2','3','4','5','6','7','8','9','0']
ops = ['A','B','C','D']

def scan():
    for j, col in enumerate(cols):
        col.value(1)
        for i, row in enumerate(rows):
            if row.value() == 1:
                time.sleep(0.2)
                return keys[i][j]
        col.value(0)
    return None


op_symbols = {
    'A': '+',
    'B': '-',
    'C': '*',
    'D': '/'
}

# Variables
num1 = None
num2 = None
operation = None
state = "num1"

def display():
    oled.fill(0)
    
    # First line: num1
    if num1 is not None:
        oled.text(str(num1), 0, 0)
    
    # Show operator as symbol instead of A/B/C/D
    if operation is not None:
        oled.text(op_symbols[operation], 60, 0)
    
    # Show num2
    if num2 is not None:
        oled.text(str(num2), 0, 15)
    
    oled.show()

oled.text("Calculator Ready", 0, 10)
oled.show()
time.sleep(2)

while True:
    key = scan()

    if key is None:
        continue

    # Clear everything
    if key == '*':
        num1 = None
        num2 = None
        operation = None
        state = "num1"
        oled.fill(0)
        oled.text("Cleared", 0, 10)
        oled.show()
        time.sleep(1)
        continue

    # Input first number
    if state == "num1":
        if key in nums:
            if num1 is None:
                num1 = int(key)
            else:
                num1 = num1 * 10 + int(key)

        elif key in ops and num1 is not None:
            operation = key
            state = "num2"

    # Input second number
    elif state == "num2":
        if key in nums:
            if num2 is None:
                num2 = int(key)
            else:
                num2 = num2 * 10 + int(key)

        # Calculate result
        elif key == '#' and num2 is not None:

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
                    oled.fill(0)
                    oled.text("Div by zero!", 0, 10)
                    oled.show()
                    time.sleep(2)
                    continue

            # Show result
            oled.fill(0)
            oled.text("Result:", 0, 0)
            oled.text(str(result), 0, 15)
            oled.show()
            time.sleep(3)

            # Prepare for next calculation
            num1 = result
            num2 = None
            operation = None
            state = "num1"

    display()
