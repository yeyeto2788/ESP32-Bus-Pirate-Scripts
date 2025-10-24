#
# Run a custom LED "snake" animation using fill/set/reset commands.
# This example uses a moving light effect with a trailing tail.
#

import time

from bus_pirate.bus_pirate import BusPirate

##################################################
#                                                 #
#            Animation parameters                 #
#                                                 #
#################################################
LED_COUNT = 8  # Total number of LEDs
HEAD_COLOR = "blue"  # Head color
TAIL_COLOR = "white"  # Tail color
DELAY = 0.1  # Delay between each frame (in seconds)
CYCLES = 3  # How many times to go back and forth
##################################################

# Connect to Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

# Change to LED mode
bp.change_mode("led")
bp.send("reset")
bp.wait()

print(f"Running snake animation with {LED_COUNT} LEDs...")

# Run animation
for _cycle in range(CYCLES):
    # Forward
    for index in range(LED_COUNT):
        bp.send("reset")
        if index > 0:
            bp.send(f"set {index - 1} {TAIL_COLOR}")
        bp.send(f"set {index} {HEAD_COLOR}")
        bp.wait()
        time.sleep(DELAY)

    # Backward
    for index in reversed(range(LED_COUNT)):
        bp.send("reset")
        if index < LED_COUNT - 1:
            bp.send(f"set {index + 1} {TAIL_COLOR}")
        bp.send(f"set {index} {HEAD_COLOR}")
        bp.wait()
        time.sleep(DELAY)

# Cleanup
bp.send("reset")
bp.wait()
bp.stop()
print("Animation finished.")
