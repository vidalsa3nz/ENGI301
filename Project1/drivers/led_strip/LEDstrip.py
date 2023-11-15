import time
import opc


class LEDStripController:
    
    def __init__(self, address='localhost:7890', length=30):
        self.address = address
        self.length = length
        self.client = opc.Client(self.address)
        
        # Test if it can connect
        if self.client.can_connect():
            print(f'Connected to {self.address}')
        else:
            print(f'WARNING: Could not connect to {self.address}')
    
    def initialize_leds(self):
        self.leds = [(255, 255, 255)] * self.length
        if not self.client.put_pixels(self.leds, channel=0):
            print('Not connected to LED strip')

    def set_led_color(self, color):
        self.leds = [color] * self.length
        if not self.client.put_pixels(self.leds, channel=0):
            print('Not connected to LED strip')
    
    def task(self):
        while True:
            print("Loop")
            for i in range(0, 255):
                for j in range(self.length):
                    self.leds[j] = (i, i, i)
    
                if not self.client.put_pixels(self.leds, channel=0):
                    print('Not connected to LED strip')
                
                time.sleep(0.1)

if __name__ == '__main__':
    try:
        led_controller = LEDStripController()  # Instantiate the LED strip controller
        
        led_controller.initialize_leds()  # Initialize LEDs with a default color
        
        # Start the LED strip control task
        led_controller.task()
        
    except KeyboardInterrupt:
        print("Program terminated by user.")
