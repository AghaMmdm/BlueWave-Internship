from machine import Pin,I2C
from pyb import Pin 
import bluelib
import time
from pyb import LED


i2c=I2C(2)
device=i2c.scan()

oled=bluelib.BOled_I2C(128,32,i2c)
oled.fill(0)
oled.text("Get start",0,20)
oled.show()

led = LED(1)
state=0

p_in = Pin('X20', Pin.IN)# Set X2 as a INPUT – Enable Inside PULL-Up Resistor
sensore = p_in.value()
led.off()
time.sleep(2)

while True:
    sensore = p_in.value()
    print(sensore)
    if sensore == 1:
        led.on()
        if state == 0:
            oled.fill(0)
            oled.text("Touched",0,20)
            oled.show()
            state=1
        
    else:
        led.off()
        time.sleep_ms(2)
        if state == 1:
             oled.fill(0)
             oled.text("not Touched",0,20)
             oled.show()
             state=0
