#
# Dump the contents of an I2C EEPROM in a file (hex/ascii format)
# Please provide the "EEPROM_ADDRESS" and "EEPROM_TYPE" variables below
# The file will be saved in the current directory
#

import os
import time
from enum import Enum

from bus_pirate.bus_pirate import BusPirate


class EEPROM_TYPES(Enum):
    EEPROM_25X010 = 1
    EEPROM_25X020 = 2
    EEPROM_25X040 = 3
    EEPROM_25X080 = 4
    EEPROM_25X160 = 5
    EEPROM_25X320 = 6
    EEPROM_25X640 = 7
    EEPROM_25X128 = 8
    EEPROM_25X256 = 9
    EEPROM_25X512 = 10
    EEPROM_25X1024 = 11
    EEPROM_25XM01 = 12
    EEPROM_25XM02 = 13
    EEPROM_25XM04 = 14


##########################################################
#                                                          #
#  Change to the desired I2C address and EEPROM type here  #
#                                                          #
##########################################################
EEPROM_ADDRESS = 0x50
EEPROM_TYPE = EEPROM_TYPES.EEPROM_24X64
############################################################

# Connect to the Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

bp.send("8")  # quit eeprom shell in case already in it
bp.wait()
bp.receive()  # Clear echoes

# Change to I2C mode
bp.change_mode("I2C")

# Enter eeprom shell and select the eeprom type
bp.send("eeprom " + hex(EEPROM_ADDRESS))
bp.wait()
bp.send(str(EEPROM_TYPE.value))
bp.wait()
bp.receive()  # Clear echoes
bp.send("5")  # 5 is the dump eeprom index
bp.clear_echoes()
bp.wait()

# Read the EEPROM
print("Reading I2C EEPROM. It may take some time...")
response = bp.receive_all()

# Clean up the response
cleaned = []
for line in response:
    if "=== I2C EEPROM Shell ===" in line:
        break
    cleaned.append(line)

# Display the dump
print("EEPROM Dump:")
for line in cleaned:
    print(line)

# Output path
timestamp = time.time()
output_path = os.path.join(os.getcwd(), f"i2c_eeprom_{timestamp}.hexdump")

# Write to the file
with open(output_path, "w") as f:
    for line in cleaned:
        f.write(line + "\n")

print(f"\nDump save at: {output_path}")

# Close the connection
bp.stop()
