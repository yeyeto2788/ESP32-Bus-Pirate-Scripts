#
# Send device-b-gone (off all devices) command endlessly.
#

from bus_pirate.bus_pirate import BusPirate

# Connect to the Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

# Change to Infrared mode
bp.change_mode("infrared")

while True:
    # Send device-b-gone command
    bp.send("devicebgone")
    bp.wait(1)

    # Read and print all lines until end of the response
    while True:
        response = bp.receive(skip=0)
        if not response:
            break
        for line in response:
            print(" -", line)
