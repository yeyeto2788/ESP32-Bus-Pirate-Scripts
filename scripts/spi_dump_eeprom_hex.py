#
# Dump the contents of an SPI EEPROM in a file (hex/ascii format)
# Change the "EEPROM_TYPE" variable below to select the EEPROM type
# The file will be saved in the current directory
#
from bus_pirate.bus_pirate import BusPirate
from bus_pirate.constants import EEPROM_TYPES
import os
import time

###########################################
#                                           #
#  Change to the desired EEPROM type here   #
#                                           #
##########################################
EEPROM_TYPE = EEPROM_TYPES.EEPROM_25X256
###########################################

# Connect to the Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

bp.send("8")  # quit flash shell in case already in it
bp.wait()
bp.receive()  # Clear echoes

# Change to SPI mode
bp.change_mode("spi")

# Enter eeprom shell and select the eeprom type
bp.send("eeprom")
bp.wait()
bp.send(str(EEPROM_TYPE.value))  # Send the selected eeprom type
bp.wait()
bp.receive_all(1)  # Clear shell echoes
bp.send("5")  # 6 is the dump hex eeprom index
bp.wait()
bp.clear_echoes(3)

# Read the EEPROM
print("Reading SPI EEPROM. It may take some time...")
response = bp.receive_all()

# Clean up the response
cleaned = []
for line in response:
    if "=== SPI EEPROM Shell ===" in line:
        break
    cleaned.append(line)

# Output path
timestamp = time.time()
output_path = os.path.join(os.getcwd(), f"spi_eeprom_{timestamp}.hexdump")

# Write to the file
with open(output_path, "w") as f:
    for line in cleaned:
        f.write(line + "\n")

print(f"\nDump save at: {output_path}")

# Close the connection
bp.stop()
