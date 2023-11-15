#!/bin/bash

# Navigate to the LED server directory
cd /var/lib/cloud9/ENGI301/Project1/drivers/led_strip

./configure_pins.sh
# Run the LED server with the specified configuration
./opc-server --config config.json &

# Navigate to your project directory
cd /var/lib/cloud9/ENGI301/Project1/drivers

# Run your Python script
PYTHONPATH=/var/lib/cloud9/ENGI301/Project1/drivers python3 main.py
