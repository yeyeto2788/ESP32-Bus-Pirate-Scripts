# 
# Dump the contents of an I2C EEPROM in a file 
# Please provide the "addr" and "eeprom" variables below
# The file will be saved in the current directory
#

from bus_pirate.bus_pirate import BusPirate
import os, time

# Supported EEPROM Ids
EEPROM_24X01   = 1
EEPROM_24X02   = 2
EEPROM_24X04   = 3
EEPROM_24X08   = 4
EEPROM_24X16   = 5
EEPROM_24X32   = 6
EEPROM_24X64   = 7
EEPROM_24X128  = 8
EEPROM_24X256  = 9
EEPROM_24X512  = 10
EEPROM_24X1025 = 11
EEPROM_24X1026 = 12
EEPROM_24XM01  = 13
EEPROM_24XM02  = 14

 ##########################################################
#                                                          #
#  Change to the desired I2C address and EEPROM type here  #
#                                                          #    
 ##########################################################
addr = 0x50
eeprom = EEPROM_24X64
############################################################

# Connect to the Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

bp.send("7") # quit eeprom shell in case already in it
bp.wait()
bp.receive()  # Clear echoes

# Change to I2C mode
bp.change_mode("I2C")

# Enter eeprom shell and select the eeprom type
bp.send("eeprom " + hex(addr))
bp.wait()
bp.send(str(eeprom))
bp.wait()
bp.receive()  # Clear echoes
bp.send("5")  # 5 is the dump eeprom index
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
