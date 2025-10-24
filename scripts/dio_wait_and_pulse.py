#
# Wait until a pin goes LOW, then send a pulse on another pin.
# You can define the pins and pulse duration below.
#

from bus_pirate.bus_pirate import BusPirate

READ_PIN = 2  # Pin to monitor for LOW state
PULSE_PIN = 3  # Pin to send the pulse to
PULSE_DURATION = 500  # Pulse duration in us (500 = 0.5 ms)

# Connect to the Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

# Swith mode to DIO
bp.change_mode("DIO")

# Wait for pin LOW and send pulse
print(f"Waiting for pin {READ_PIN} to go LOW...")
while True:
    bp.send(f"read {READ_PIN}")
    bp.wait(0.05)
    state = bp.receive()
    if any("= 0" in line.upper() for line in state):
        print(
            f"Pin {READ_PIN} is LOW. Sending pulse to pin {PULSE_PIN} ({PULSE_DURATION} µs)."
        )
        bp.send(f"pulse {PULSE_PIN} {PULSE_DURATION}")
        bp.wait()
        break

# Done
bp.stop()
print("Pulse sent. Exiting.")
