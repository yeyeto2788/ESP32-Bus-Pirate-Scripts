#
# Sniff and log all WiFi packets with timestamp.
# This script records all packets received during the defined duration.
# The file will be saved in the current directory
#

import os
import time

from bus_pirate.bus_pirate import BusPirate

DURATION = 600  # Duration of the sniffing in seconds

# Connect to the Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

# Change to WiFi mode
bp.change_mode("wifi")

# Prepare log file (current directory)
timestamp = int(time.time())
filename = f"wifi_sniff_log_{timestamp}.txt"
filepath = os.path.join(os.getcwd(), filename)

# Start sniffing
bp.send("sniff")
bp.wait()
bp.clear_echoes(2)
print("Sniffing started... Logging for", DURATION, "seconds.")

# Logging loop
start_time = time.time()
with open(filepath, "a") as f:
    while time.time() - start_time < DURATION:
        lines = bp.receive(skip=0)
        if lines:
            log_time = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n--- Sniff at {log_time} ---\n")
            for line in lines:
                f.write(line + "\n")
            print(f"Sniff logged at {log_time} ({len(lines)} lines).")

# Close the connection
print("\nSniffing finished.")
bp.stop()
