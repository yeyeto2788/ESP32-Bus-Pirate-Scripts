#
# Wait until a pin goes LOW, then send a pulse on another pin.
# You can define the pins and pulse duration below.
#

read_pin = 2          # Pin to monitor for LOW state
pulse_pin = 3         # Pin to send the pulse to
pulse_duration = 500  # Pulse duration in us (500 = 0.5 ms)

from bus_pirate.bus_pirate import BusPirate

# Connect to the Bus Pirate
bp = BusPirate.auto_connect()
bp.start()

# Swith mode to DIO
bp.change_mode("DIO")

# Wait for pin LOW and send pulse
print(f"Waiting for pin {read_pin} to go LOW...")
while True:
    bp.send(f"read {read_pin}")
    bp.wait(0.05)
    state = bp.receive()
    if any("= 0" in line.upper() for line in state):
        print(f"Pin {read_pin} is LOW. Sending pulse to pin {pulse_pin} ({pulse_duration} µs).")
        bp.send(f"pulse {pulse_pin} {pulse_duration}")
        bp.wait()
        break

# Done
bp.stop()
print("Pulse sent. Exiting.")
