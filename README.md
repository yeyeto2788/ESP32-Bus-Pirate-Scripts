# ESP32 Bus Pirate Scripts

![Bus Pirate Scripts](bus_pirate_scripts.png)

A collection of **easy-to-use** Python scripts to control the [**ESP32 Bus Pirate**](https://github.com/geo-tp/ESP32-Bus-Pirate) via USB serial interface.

## Scripts

| Script | Description |
|--------|-------------|
| `wifi_scan_log.py` | Periodically scan networks and logs them timestamped to a file |
| `wifi_sniff_log.py` | Periodically sniff WiFi and logs timestamped raw packets to a file |
| `wifi_deauth_all.py` | Sends deauth frames to all discovered SSIDs |
| `bluetooth_sniff_log.py` | Periodically sniff packets and logs them timestamped to a file |
| `uart_read_log.py` | Logs all UART data receiveid into a file |
| `i2c_dump_eeprom_hex.py` | Dump the content of an I2C EEPROM in hex format to a file |
| `i2c_dump_eeprom_bin.py` | Dump the content of an I2C EEPROM in raw bin format to a file |
| `i2c_identify_all.py` | Detects all I2C devices and attempts to identify them |
| `i2c_glitch_all.py` | Detects all I2C devices and attempts to glitch them |
| `spi_dump_flash_hex.py` | Dump the content of an SPI Flash in hex format to a file |
| `spi_dump_flash_bin.py` | Dump the content of an SPI Flash in raw bin format to a file |
| `spi_dump_eeprom_hex.py` | Dump the content of an SPI EEPROM in hex format to a file |
| `spi_dump_eeprom_bin.py` | Dump the content of an SPI EEPROM in raw bin format to a file |
| `led_custom_animation.py` | Custom LED animation using led commands |
| `infrared_devicebgone_loop.py` | Sends 'Device-B-Gone' IR commands in loop |
| `dio_wait_and_pulse.py`  | Wait for a defined pin to go LOW to send a pulse |

**Each script:**
- Auto-detects the ESP32 Bus Pirate
- Switches to the correct mode automatically
- Logs output to console and/or file
- Save the output file in the current directory

## Requirements

- Python 3.7 or higher
- `pyserial` Python library

Install dependencies:
```bash
pip install -r requirements.txt
```

---

##  Getting Started

1. Download the scripts folder
2. Plug in your Bus Pirate device via USB serial
3. Run any script using Python:
```bash
python3 wifi_scan_log.py
```

**Note:** If needed, you can manually configure the pin via serial for any mode before launching the script.

## Create Your Script

The `BusPirate` class abstracts serial communication and provides methods like:

```python
from bus_pirate.bus_pirate import BusPirate

bp = BusPirate.auto_connect()  # Auto-detect the ESP32 Bus Pirate
bp.start()                     # Init connection + clear 
bp.change_mode("dio")          # Switch to I2C, UART, WiFi, etc.
bp.send("set 1 LOW")           # Send a command (string)
bp.wait()                      # Wait for response (default 300ms)
lines = bp.receive()           # Read lines from the device
lines = bp.receive_all(2)      # Read lines from the device until a given silent time
bp.stop()                      # Close connection
```

Additional `Helper` class to parse and manipulate response from the ESP32 Bus Pirate.


## Project Structure

```
scripts/
├── bus_pirate/        # Bus Pirate class
│   ├── bus_pirate.py
│   └── helper.py
├── bluetooth_sniff_log.py
├── dio_wait_and_pulse.py
└── ...
```


---