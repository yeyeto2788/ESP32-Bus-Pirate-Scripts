# 
# Dump the contents of an SPI NOR FLASH in a file (hex/ascii format)
# The file will be saved in the current directory
#

from bus_pirate.bus_pirate import BusPirate
import os, time

# Connect to the Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

bp.send("9") # quit flash shell in case already in it
bp.wait()
bp.receive()  # Clear echoes

# Change to SPI mode
bp.change_mode("spi")

# Enter flash shell and select the flash type
bp.send("flash")
bp.wait()
bp.receive_all(1)  # Clear shell echoes
bp.send("7")  # 7 is the dump hex flash index
bp.wait()
bp.clear_echoes(3)

# Read the FLASH
print("Reading SPI FLASH. It may take some time...")
response = bp.receive_all()

# Clean up the response
cleaned = []
for line in response:
    if "=== SPI Flash Shell ===" in line:
        break
    cleaned.append(line)

# Output path
timestamp = time.time()
output_path = os.path.join(os.getcwd(), f"spi_flash_{timestamp}.hexdump")

# Write to the file
with open(output_path, "w") as f:
    for line in cleaned:
        f.write(line + "\n")

print(f"\nDump save at: {output_path}")

# Close the connection
bp.stop()
