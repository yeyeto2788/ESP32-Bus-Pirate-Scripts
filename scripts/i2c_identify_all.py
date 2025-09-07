# 
# Scan and identify all I2C devices on the bus
#

from bus_pirate.bus_pirate import BusPirate
from bus_pirate.helper import Helper

# Connect to the Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

# Change to I2C mode
bp.change_mode("I2C")

# Scan I2C bus and get results
bp.send("scan")
print("Scanning I2C bus, it may take few seconds...")
bp.wait(2)
results = bp.receive(skip=1) # echo

# Extract addresses from results
addr_list = Helper.extractHexFromList(results)
print("Found addresses: ", addr_list)

# Identify each address
for addr in addr_list:
    bp.send(f"identify {addr}")
    bp.wait()
    lines = bp.receive_all()
    for line in lines:
        print(" - " + line)

# Close the connection
bp.stop()
