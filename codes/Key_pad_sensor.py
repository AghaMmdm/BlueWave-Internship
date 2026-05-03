from machine import Pin
import time

rows = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in ["X22", "X21", "X20", "X19"]]


cols = [Pin(i, Pin.OUT) for i in ["X4", "X3", "X2", "X1"]]

keys = [
    ['1', '4', '7', '*'],
    ['2', '5', '8', '0'],
    ['3', '6', '9', '#'],
    ['A', 'B', 'C', 'D']
]

nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def scan():
    for j, col in enumerate(cols):
        col.value(1)
        for i, row in enumerate(rows):
            if row.value() == 1:
                print("Pressed:", keys[i][j])
                time.sleep(0.3)
                return keys[i][j]
        col.value(0)

num1 = 0
num2 = 0

while True:
    temp = scan()
    if temp in nums:
        if num1 == 0:
            num1 = int(temp)
        else:
            num2 = int(temp)
            
    if temp == 'A':
        print("Sum:", num1 + num2)
        num1 = 0
        num2 = 0
        
    if temp == 'B':
        print("Difference:", num1 - num2)
        num1 = 0
        num2 = 0
        
    if temp == 'C':
        print("Product:", num1 * num2)
        num1 = 0
        num2 = 0
        
    if temp == 'D':
        if num2 != 0:
            print("Quotient:", num1 / num2)
        else:
            print("Error: Division by zero")
        num1 = 0
        num2 = 0
        
    if temp == '*':
        print("Cleared")
        num1 = 0
        num2 = 0
        
    if temp == '#':
        print("Exiting")
        break

