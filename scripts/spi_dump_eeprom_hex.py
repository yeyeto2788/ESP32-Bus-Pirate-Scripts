# 
# Dump the contents of an SPI EEPROM in a file (hex/ascii format)
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

# Connect to the Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

bp.send("8") # quit flash shell in case already in it
bp.wait()
bp.receive()  # Clear echoes

# Change to SPI mode
bp.change_mode("spi")

# Enter eeprom shell and select the eeprom type
bp.send("eeprom")
bp.wait()
bp.send(str(eeprom))  # Send the selected eeprom type
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
