# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Buzzer
--------------------------------------------------------------------------
License:   
Copyright 2021-2023 Vidal Saenz

Based on library from

Copyright 2018 Nicholas Lester

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
This file provides an interface to a PWM controllered buzzer.
  - Ex:  https://www.adafruit.com/product/1536


APIs:
  - Buzzer(pin)
    - play(frequency, length=1.0, stop=False)
      - Plays the frequency for the length of time

    - stop(length=0.0)
      - Stop the buzzer (will cause breaks between tones)
      
    - cleanup()
      - Stop the buzzer and clean up the PWM

"""
import time

import Adafruit_BBIO.PWM as PWM

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Main Tasks
# ------------------------------------------------------------------------

class Buzzer():
    pin       = None
    
    def __init__(self, pin):
        self.pin = pin
 
        # NOTE:  No other setup required
 
    # End def
    
    
    def play(self, frequency, length=0.5, stop=False):
        """ Plays the frequency for the length of time.
            frequency - Value in Hz or None for no tone
            length    - Time in seconds (default 1.0 seconds)
            stop      - Stop the buzzer (will cause breaks between tones)
        """
        if frequency is not None:
            # !!! FIX !!! 
            print("Playing {0}".format(frequency))
            PWM.start(self.pin, duty_cycle=50, frequency=frequency, polarity=0)
            # !!! FIX !!! 
            
        time.sleep(length)
        
        if (stop):
            self.stop()
        
    # End def

    
    def stop_buzzer(self):
        """ Stops the buzzer immediately """
        PWM.stop(self.pin)
        
    def stop(self, length=0.5):
        """ Stops the buzzer (will cause breaks between tones)
            length    - Time in seconds (default 0.0 seconds)
        """
        # !!! FIX !!! 
        print("Stopping the buzzer")
        PWM.stop(self.pin)
        # !!! FIX !!! 
        

        time.sleep(length)
        
    # End def

    
    def cleanup(self):
        """Stops the buzzer and cleans up the PWM.
             *** This function must be called during hardware cleanup ***
        """
        self.stop()
        PWM.cleanup()
    # End def
    
# End class

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

NOTES = {
    'C': 261.63,
    'D': 293.66,
    'E': 329.63,
    'F': 349.23,
    'G': 392.00,
    'A': 440.00,
    'B': 493.88,
    'REST': None  # Represents a rest (no tone)
}

# Durations for notes (in seconds)
DURATIONS = {
    'Q': 0.0025,  # Quarter note
    'H': 0.005,  # Half note
    'W': 0.01,  # Whole note
}

# Melody for the chorus of "Levitating" by Dua Lipa
LEVITATING_CHORUS_MELODY = [
    ('D', 'Q'), ('E', 'H'), ('D', 'H'), ('E', 'W'),
    ('E', 'Q'), ('D', 'H'), ('D', 'H'), ('E', 'W'),
    ('G', 'Q'), ('A', 'H'), ('G', 'H'), ('A', 'W'),
    ('A', 'Q'), ('G', 'H'), ('G', 'H'), ('A', 'W')
]

if __name__ == '__main__':
    try:
        buzzer = Buzzer("P2_1")  # Replace "YOUR_PIN_NAME" with the actual pin name
        
        for note, duration in LEVITATING_CHORUS_MELODY:
            frequency = NOTES[note]
            duration_sec = DURATIONS[duration]
            buzzer.play(frequency, duration_sec, stop=True)  # Play the note and stop before the next note
        
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping the buzzer...")
        buzzer.stop_buzzer()  # Stop the buzzer when Ctrl+C is pressed
        buzzer.cleanup()  # Clean up PWM resources
        
    except Exception as e:
        print("Error: ", str(e))
        buzzer.cleanup()  # Clean up PWM resources in case of other exceptions
        
        
    # print("Buzzer Test")
    
    # buzzer = Buzzer("P2_1")
    
    # print("Play tone")
    
    # buzzer.play(440, 1.0, False)      # Play 440Hz for 1 second
    # time.sleep(1.0)
    # buzzer.play(880, 1.0, True)       # Play 440Hz for 1 second
    # time.sleep(1.0)   

    # buzzer.cleanup()
    
    # print("Test Complete")

