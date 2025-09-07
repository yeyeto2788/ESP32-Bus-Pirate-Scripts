#
# Read and log all UART data.
# This script records all incoming UART data during the defined duration.
# The file will be saved in the current directory.
#

duration = 600  # Duration of the logging in seconds

from bus_pirate.bus_pirate import BusPirate
import time
import os

# Connect to the Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

# Change to UART mode
bp.change_mode("uart")

# Prepare log file (current directory)
timestamp = int(time.time())
filename = f"uart_read_log_{timestamp}.txt"
filepath = os.path.join(os.getcwd(), filename)

# Start UART read mode
bp.send("read")
bp.wait()
bp.clear_echoes(2)
print("UART read started... Logging for", duration, "seconds.")

# Logging loop
start_time = time.time()
with open(filepath, "a") as f:
    while time.time() - start_time < duration:
        lines = bp.receive(skip=0)
        if lines:
            for line in lines:
                f.write(line + "\n")
                print(f"UART read logged ({len(lines)} lines).")

# Close the connection
print("\nUART logging finished.")
bp.stop()
