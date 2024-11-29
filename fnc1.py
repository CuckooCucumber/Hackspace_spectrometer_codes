from adafruit_as7341 import AS7341
import time
import board
import busio
import digitalio
import pwmio
import math

class serial_dilution():
    def __init__(self, sensor, led):
        self.n_samples = int(input("Enter the Number of Samples: "))
        self.n_replicates = int(input("Enter the Number of Replicates: "))
        self.sensor = sensor
        self.led = led
        pass

    def setintegration(self, intTime):
        stepSize = 9999
        self.sensor.astep = stepSize
        self.sensor.atime = int(intTime*1000/(2.78*(stepSize+1)))
        print("Integration Time set to " + str(((1+self.sensor.atime)*(1+self.sensor.astep)*0.00278)) + " ms")

    def read(self, wavelength, brightness) -> int:
        wavelengths = [415,445,480,515,555,590,630,680]
        sensor_channels = self.sensor.all_channels
        print("415nm " + str(sensor_channels[0]))
        print("445nm " + str(sensor_channels[1]))
        print("480nm " + str(sensor_channels[2]))
        print("515nm " + str(sensor_channels[3]))
        print("555nm " + str(sensor_channels[4]))
        print("590nm " + str(sensor_channels[5]))
        print("630nm " + str(sensor_channels[6]))
        print("680nm " + str(sensor_channels[7]))
        sesor_reading = dict(zip(wavelengths, sensor_channels))
        trans = (sesor_reading[wavelength]/brightness)
        absorbance = -1* math.log(trans,10)
        print(absorbance)
        return sesor_reading[wavelength]


    def final_reading(self, wavelength: int, brightness_percentage: int = 100, integration_time : int = 100, sensor_gain : int = 7) -> dict:
        result_dict = {}
        print("Calibrating LED brightness")
        brightness = brightness_percentage * 650.25
        self.led.duty_cycle = int(brightness)
        print(f"LED calibrated to {brightness_percentage} percentage")
        print("\n")
        print("Setting up Gain in sensor")
        self.sensor.gain = sensor_gain
        print(f"Sensor gain set to {sensor_gain}")
        print("\n")
        print("Setting up sensor integration time")
        self.setintegration(integration_time)
        print("\n")
        print("Getting ready for samples...")
        for i in range(self.n_replicates):
            result_dict[f'replicate_{i}'] = {}
            print(f"Replicate {i+1}")
            print("Time to read the control!")
            input("Press Enter once you have loaded the control: ")
            ctrl_brightness = self.read(wavelength, brightness)
            for j in range(self.n_samples):
                input(f"Press Enter once you have loaded the sample {j+1}: ")
                result_dict[f'replicate_{i}'][f'sample_{j+1}'] = self.read(wavelength, ctrl_brightness)
        return(result_dict)
