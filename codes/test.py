import bluelib
import time
from machine import I2C
from pyb import Pin, ADC

# =========================
# Set pins
# =========================
adc = ADC(Pin("X19"))          # LDR pin
led_r = 0
led_g = 0
led_b = 0
brgb = bluelib.BRGB(Pin("X1"),2)

# =========================
# Settings
# =========================
SAMPLES = 20
SETTLE_TIME = 0.05

# Coefficients
GAIN_R = 1.0
GAIN_G = 1.0
GAIN_B = 1.8

# =========================
# Helper Functions
# =========================
def read_avg():
    total = 0
    for _ in range(SAMPLES):
        total += adc.read()
        time.sleep_ms(2)
    return total / SAMPLES


def turn_off_all():
    led_r = 0
    led_g = 0
    led_b = 0
    color = (led_g, led_r, led_b)
    brgb.fill(color)
    brgb.write()


def measure_channel(r, g, b):
    turn_off_all()
    led_r = r
    led_g = g
    led_b = b
    color = (led_g, led_r, led_b)
    brgb.fill(color)
    brgb.write()
    time.sleep(SETTLE_TIME)
    value = read_avg()
    turn_off_all()
    return value


# =========================
# Remove ambient light
# =========================
def measure_with_ambient_subtraction(r, g, b):
    ambient = measure_channel(0, 0, 0)      # ambient light
    color = measure_channel(r, g, b)        # LED light
    value = color - ambient
    if value < 0:
        value = 0
    return value


# =========================
# White calibration
# =========================
def calibrate_white():
    print("Please place a white surface under the sensor...")
    time.sleep(3)

    wr = measure_with_ambient_subtraction(1,0,0)
    wg = measure_with_ambient_subtraction(0,1,0)
    wb = measure_with_ambient_subtraction(0,0,1)

    print("White Calibration Done")
    return wr, wg, wb


# =========================
# Final color proccessing 
# =========================
def process_color(r, g, b, wr, wg, wb):

    wr = max(wr, 1)
    wg = max(wg, 1)
    wb = max(wb, 1)

    # Normalization to white
    r = (r / wr) * GAIN_R
    g = (g / wg) * GAIN_G
    b = (b / wb) * GAIN_B

    r = max(r, 0)
    g = max(g, 0)
    b = max(b, 0)

    # =========================
    # Relative Normalization
    # =========================
    total = r + g + b
    if total == 0:
        return 0, 0, 0

    r = r / total
    g = g / total
    b = b / total

    # =========================
    # Smart Clamp Third Color Noise Reduction
    # =========================
    if b < (r + g) / 6:
        b = 0
    if r < (g + b) / 6:
        r = 0
    if g < (r + b) / 6:
        g = 0

    # Scale to 0 to 255
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    return r, g, b


# =========================
# Main program
# =========================
white_r, white_g, white_b = calibrate_white()

while True:

    raw_r = measure_with_ambient_subtraction(1,0,0)
    raw_g = measure_with_ambient_subtraction(0,1,0)
    raw_b = measure_with_ambient_subtraction(0,0,1)

    R, G, B = process_color(raw_r, raw_g, raw_b,
                             white_r, white_g, white_b)

    print("RGB:", R, G, B)

    time.sleep(1)
