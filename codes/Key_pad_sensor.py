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

def scan():
    for j, col in enumerate(cols):
        col.value(1)
        for i, row in enumerate(rows):
            if row.value() == 1:
                print("Pressed:", keys[i][j])
                time.sleep(0.3)
        col.value(0)

while True:
    scan()

