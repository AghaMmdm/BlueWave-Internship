from machine import Pin, SPI
from mfrc522 import MFRC522
import time

# SPI Configuration for Pyboard/STM32
# Pins X6 (SCK), X7 (MISO), and X8 (MOSI) are hardware-managed by SPI(1)
spi = SPI(1, baudrate=2500000)

# Control Pins Definition
cs = 'X5'
rst = 'X4'

# Initialize the MFRC522 sensor object
rdr = MFRC522(spi, cs, rst)

print("--- RFID Reader Ready ---")
print("Place your tag near the reader...")

while True:
    # Scan for cards/tags
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    
    if stat == rdr.OK:
        # Anti-collision: Get the UID of the card
        (stat, raw_uid) = rdr.anticoll()
        
        if stat == rdr.OK:
            print("\nNew Card Detected!")
            # Format UID as a Hexadecimal string
            uid = "%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            print("Card ID: ", uid)
            
            # Delay to avoid multiple readings of the same card
            time.sleep(1)
