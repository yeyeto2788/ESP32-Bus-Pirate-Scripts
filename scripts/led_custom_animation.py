#
# Run a custom LED "snake" animation using fill/set/reset commands.
# This example uses a moving light effect with a trailing tail.
#

from  bus_pirate.bus_pirate import BusPirate
import time
 
 ##################################################
#                                                 #
#            Animation parameters                 #
#                                                 #
 #################################################
led_count = 8                 # Total number of LEDs
head_color = "blue"           # Head color
tail_color = "white"          # Tail color
delay = 0.1                   # Delay between each frame (in seconds)
cycles = 3                    # How many times to go back and forth
##################################################

# Connect to Bus Pirate 
bp = BusPirate.auto_connect()
bp.start()

# Change to LED mode
bp.change_mode("led")
bp.send("reset")
bp.wait()

print(f"Running snake animation with {led_count} LEDs...")

# Run animation
for cycle in range(cycles):
    # Forward
    for i in range(led_count):
        bp.send("reset")
        if i > 0:
            bp.send(f"set {i-1} {tail_color}")
        bp.send(f"set {i} {head_color}")
        bp.wait()
        time.sleep(delay)

    # Backward
    for i in reversed(range(led_count)):
        bp.send("reset")
        if i < led_count - 1:
            bp.send(f"set {i+1} {tail_color}")
        bp.send(f"set {i} {head_color}")
        bp.wait()
        time.sleep(delay)

# Cleanup
bp.send("reset")
bp.wait()
bp.stop()
print("Animation finished.")
