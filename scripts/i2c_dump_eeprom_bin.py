#
# Dump the contents of an I2C EEPROM in a file (bin format)
# Please provide the "EEPROM_ADDRESS" and "EEPROM_TYPE" variables below
# The file will be saved in the current directory
#

from bus_pirate.bus_pirate import BusPirate
from bus_pirate.constants import EEPROM_TYPES
import os
import time

##########################################################
#                                                          #
#  Change to the desired I2C address and EEPROM type here  #
#                                                          #
##########################################################
EEPROM_ADDRESS = 0x50
EEPROM_TYPE = EEPROM_TYPES.EEPROM_24X64
############################################################

# End markers for parsing
END_MARKER = b"=== I2C EEPROM Shell ==="

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
bp.send("6")  # 6 is the dump raw eeprom index
bp.wait()
bp.send("y")  # confirm
bp.clear_echoes(2)
bp.wait()

# Read the EEPROM
print("Reading I2C EEPROM. It may take some time...")
response = bp.receive_raw(2)

# Output path
timestamp = time.time()
output_path = os.path.join(os.getcwd(), f"i2c_eeprom_{timestamp}.bin")

## Clean up the response
pos_end = response.find(END_MARKER)
if pos_end != -1:
    response = response[:pos_end]

# Write to the file
with open(output_path, "wb") as f:
    f.write(response)

print(f"\nDump save at: {output_path}")

# Close the connection
bp.stop()
