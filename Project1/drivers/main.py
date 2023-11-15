#!/usr/bin/env python3
"""
--------------------------------------------------------------------------
Sip N' Sprout Main
--------------------------------------------------------------------------
License:   
Copyright 2023 Vidal Saenz

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
"""
from PeristalticPump import Pump
from SoilSensor import Moisture
from potentiometer import Potentiometer
from hd44780 import LCD
from light import Light
import Adafruit_BBIO.GPIO as GPIO
import time
import threading
import sys
sys.path.append('/var/lib/cloud9/ENGI301/Project1/drivers/led_strip')
import opc

# Pins
SOIL_SENSOR_PIN = "AIN4"
PUMP_PIN = "P2_35"
rs = "P1_2"
enable = "P1_4"
d4 = "P2_2"
d5 = "P2_4"
d6 = "P2_6"
d7 = "P2_8"
cols = 16
rows = 2

ADDRESS = 'localhost:7890'

# Create a client object
client = opc.Client(ADDRESS)

# Test if it can connect
if client.can_connect():
    print ('connected to %s' % ADDRESS)
else:
    # We could exit here, but instead let's just print a warning
    # and then keep trying to send pixels in case the server
    # appears later
    print ('WARNING: could not connect to %s' % ADDRESS)

# Define Pixel String
STR_LEN=90
#30 Leds
for i in range(STR_LEN):
    leds = [(255, 255, 255)] * STR_LEN

if not client.put_pixels(leds, channel=0):
    print ('not connected')

time.sleep(0.1)


def set_led_intensity(lux):
    
    # Map lux readings to LED intensity (adjust the mapping based on your requirements)
    if lux > 0:
        intensity = int(((150 - lux) / 150) * 255)
    else:
        # If lux is zero or negative, set LEDs to max brightness
        intensity = 255
        
    print(intensity)
    # Update LED colors based on the intensity
    for i in range(STR_LEN):
        leds[i] = (intensity, intensity, intensity)

    # Update the LED strip
    client.put_pixels(leds, channel=0)

# Uses each light's address to set display to set a color
def task():
    while True:
        # Get lux readings from the light sensor
        lux = light.get_value()
        print(f"Lux Reading: {lux}")

        # Set LED intensity based on lux readings
        set_led_intensity(lux)

        time.sleep(1)

# Function to run the light process
def light_process():
    try:
        while True:
            # Get lux readings from the light sensor
            lux = light.get_value()
            print(f"Lux Reading: {lux}")
    
            # Set LED intensity based on lux readings
            set_led_intensity(lux)
    
            time.sleep(1)
    except KeyboardInterrupt:
    # Cleanup operations for the pump process if needed
        print("Light process terminated.")

# Function to run the pump process
def pump_process():
    try:
        while True:
            moisture_percentage = soil_sensor.get_moisture_percentage()
            print(f"Moisture Percentage = {moisture_percentage:.2f}%")
            lcd.clear()
            time.sleep(0.1) 
            lcd.setCursor(0, 0)
            lcd.message("Moisture")
            lcd.setCursor(0, 1)
            lcd.message("Level: {:.2f}%".format(moisture_percentage))
            
            if moisture_percentage < 20:
                print("Moisture lvl low. Turning on the pump.")
                lcd.clear()
                lcd.setCursor(0, 1)
                lcd.message("Running Pump")
                pump.turn_on_pump()
                time.sleep(10)  # Run the pump for 10 seconds
                pump.turn_off_pump()
                lcd.clear()
                lcd.setCursor(0, 1)
                lcd.message("Pump OFF       ")
                print("Pump turned off. Waiting for 60 seconds before checking again.")
                time.sleep(5)  # Pause for 60 seconds before checking again
            else:
                print("Moisture level is sufficient. Waiting for 10 seconds before checking again.")
                lcd.clear()
                lcd.setCursor(0, 0)
                lcd.message("Current Moisture")
                lcd.setCursor(0, 1)
                lcd.message("Level: {:.2f}%".format(moisture_percentage))
                time.sleep(10)  # Pause for 10 seconds before checking again
    except KeyboardInterrupt:
    # Cleanup operations for the pump process if needed
        print("Pump process terminated.")



if __name__ == '__main__':
    try:
        # Initialize soil sensor, pump, potentiometer, and LCD
        soil_sensor = Moisture(SOIL_SENSOR_PIN)
        pump = Pump(PUMP_PIN)
        # potentiometer = Potentiometer(POTENTIOMETER_PIN)
        lcd = LCD(rs, enable, d4, d5, d6, d7, cols, rows)
        light = Light(bus=1, address=0x23)
        
        # Create threads for light and pump processes
        light_thread = threading.Thread(target=light_process)
        pump_thread = threading.Thread(target=pump_process)
        
        # Start the threads
        light_thread.start()
        pump_thread.start()
        
        # Keep the main thread running (It won't execute any code, just waits for the threads)
        light_thread.join()
        pump_thread.join()
    
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("GPIO cleanup completed. Exiting...")
    except Exception as e:
        print(f"An exception occurred: {e}")
