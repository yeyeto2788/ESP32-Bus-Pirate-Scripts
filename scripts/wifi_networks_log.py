# 
# Scan and log all WiFi networks found in a file with timestamp.
# Please provide the "duration" variable below.
# The file will be saved in the current directory.
#

duration = 600 # Duration of the logging in seconds

from bus_pirate.bus_pirate import BusPirate
from bus_pirate.helper import Helper
import time
import os

# Search and connect to the Bus Pirate
bp = BusPirate.auto_connect()

# Initialize the Bus Pirate
bp.start()

# Change to WiFi mode
bp.change_mode("wifi")

# Prepare log file (current directory)
timestamp = int(time.time())
filename = f"wifi_networks_log_{timestamp}.txt"
filepath = os.path.join(os.getcwd(), filename)

# Logging start
start_time = time.time()
while time.time() - start_time < duration:
    # Scanner
    bp.send("scan")
    print("Scanning WiFi networks, it may take few seconds...")
    bp.wait(10)
    results = bp.receive(skip=2)

    # Timestamp
    log_time = time.strftime("%Y-%m-%d %H:%M:%S")

    # save
    with open(filepath, "a") as f:
        f.write(f"\n--- Scan at {log_time} ---\n")
        for line in results:
            f.write(line + "\n")

    # Message console
    print(f"Scan logged at {log_time} ({len(results)} networks found).")

# Close the connection
print("\nLogging finished.")
bp.stop()
