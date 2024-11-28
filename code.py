print("Loading libraries")
from adafruit_as7341 import AS7341
import time
import board
import busio
import digitalio
import pwmio
from fnc1 import serial_dilution

print("Connecting sensor")
myi2c = busio.I2C(scl=board.GP5, sda=board.GP4)
mysensor = AS7341(myi2c)

led_sensor = pwmio.PWMOut(board.GP19, frequency=1000)
led_indicator = digitalio.DigitalInOut(board.GP21)

led_indicator.direction = digitalio.Direction.OUTPUT
led_indicator.value = True

spec = serial_dilution(sensor = mysensor, led = led_sensor)
result = spec.final_reading(wavelength = 515, brightness_percent = 40)
led_indicator.value = False
