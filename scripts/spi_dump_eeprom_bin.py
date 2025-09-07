# 
# Dump the contents of an SPI NOR FLASH in a file (bin format)
# Change the "eeprom" variable below to select the EEPROM type
# The file will be saved in the current directory
#

# Supported EEPROM Ids
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

 ########################################### 
#                                           #
#  Change to the desired EEPROM type here   #
#                                           #
 ##########################################
eeprom = EEPROM_25X256
###########################################

from bus_pirate.bus_pirate import BusPirate
import os, time

# End markers for parsing
END_MARKER = b"=== SPI EEPROM Shell ==="

# Connect to the Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

bp.send("8") # quit flash shell in case already in it
bp.wait()
bp.receive()  # Clear echoes

# Change to SPI mode
bp.change_mode("spi")

# Enter flash shell and select the flash type
bp.send("eeprom")
bp.wait()
bp.send(str(eeprom))  # Send the selected eeprom type
bp.wait()
bp.send("6")  # 6 is the dump raw eeprom index
bp.wait()
bp.receive_all(1)  # Clear shell echoes
bp.send("y") # confirm
bp.wait()
bp.clear_echoes(1)

# Read the EEPROM
print("Reading EEPROM. It may take some time...")
response = bp.receive_raw(2)

## Clean up the response
pos_end = response.find(END_MARKER)
if pos_end != -1:
    response = response[:pos_end]

# Strip trailing newline if present
if response.endswith(b"\n"):
    response = response[:-1]

# Output path
timestamp = time.time()
output_path = os.path.join(os.getcwd(), f"spi_eeprom_{timestamp}.bin")

# Write to the file
with open(output_path, "wb") as f:
    f.write(response)

print(f"\nDump save at: {output_path}")

# Close the connection
bp.stop()
