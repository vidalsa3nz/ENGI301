import Adafruit_BBIO.GPIO as GPIO
import time

    def __init__(self, pin="P1_8", num_leds=30):
        self.LED_STRIP_PIN = pin
        self.NUM_LEDS = num_leds
        GPIO.setup(self.LED_STRIP_PIN, GPIO.OUT)

    def send_bit(self, bit):
        GPIO.output(self.LED_STRIP_PIN, bit)
        time.sleep(0.00002)  # Adjust this delay if needed
        GPIO.output(self.LED_STRIP_PIN, GPIO.LOW)
        time.sleep(0.00002)  # Adjust this delay if needed

    def send_byte(self, byte):
        for _ in range(8):
            self.send_bit(byte & 1 << 7)
            byte <<= 1

    def send_color(self, red, green, blue):
        self.send_byte(green)
        self.send_byte(red)
        self.send_byte(blue)

    def set_led_color(self, index, red, green, blue):
        # Start frame
        self.send_byte(0)
        self.send_byte(0)
        self.send_byte(0)
        # LED data
        for i in range(self.NUM_LEDS):
            if i == index:
                self.send_color(red, green, blue)
            else:
                self.send_color(0, 0, 0)
        # End frame
        self.send_byte(0xFF)

    def set_all_leds_color(self, red, green, blue):
        # Start frame
        self.send_byte(0)
        self.send_byte(0)
        self.send_byte(0)
        # LED data (set all LEDs to the specified color)
        for _ in range(self.NUM_LEDS):
            self.send_color(red, green, blue)
        # End frame
        self.send_byte(0xFF)

    def turn_off(self):
        # Turn off all LEDs
        self.set_all_leds_color(0, 0, 0)

    def cleanup(self):
        # Cleanup GPIO
        GPIO.cleanup()

# Example usage of the LEDStrip class
if __name__ == "__main__":
    try:
        led_strip = LEDStrip(pin="P1_8", num_leds=30)
        led_strip.set_all_leds_color(255, 0, 0)  # Set all LEDs to red
        time.sleep(5)  # Wait for 5 seconds
        led_strip.turn_off()  # Turn off all LEDs
        led_strip.cleanup()  # Cleanup GPIO

    except KeyboardInterrupt:
        # If the user interrupts the program with Ctrl+C, cleanup GPIO
        led_strip.cleanup()
