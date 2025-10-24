#
# Dump the contents of an SPI NOR FLASH in a file (bin format)
# The file will be saved in the current directory
#

import os
import time

from bus_pirate.bus_pirate import BusPirate

# End markers for parsing
END_MARKER = b"=== SPI Flash Shell ==="

# Connect to the Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

bp.send("9")  # quit flash shell in case already in it
bp.wait()
bp.receive()  # Clear echoes

# Change to SPI mode
bp.change_mode("spi")

# Enter flash shell and select the flash type
bp.send("flash")
bp.wait()
bp.send("8")  # 8 is the dump raw flash index
bp.wait()
bp.receive_all(1)  # Clear shell echoes
bp.send("y")  # confirm
bp.wait()
bp.clear_echoes(1)

# Read the FLASH
print("Reading SPI FLASH. It may take some time...")
response = bp.receive_raw(2)

## Clean up the response
pos_end = response.find(END_MARKER)
if pos_end != -1:
    response = response[:pos_end]

# Output path
timestamp = time.time()
output_path = os.path.join(os.getcwd(), f"spi_flash_{timestamp}.bin")

# Write to the file
with open(output_path, "wb") as f:
    f.write(response)

print(f"\nDump save at: {output_path}")

# Close the connection
bp.stop()
