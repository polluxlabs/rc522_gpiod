Of course. Here is the text for your `README.md` file, correctly formatted for GitHub.

Simply copy the entire content from the block below and paste it into the `README.md` file in your GitHub repository. GitHub will automatically render it into a well-formatted page.

-----

# Lean RC522 Python Library for Raspberry Pi 5

A minimalist and easy-to-integrate Python library for controlling the RC522 RFID reader via the SPI interface on a Raspberry Pi 5.

This project was created to provide a straightforward solution without heavy dependencies. The entire library is contained within a single file to make integration into your own projects as simple as possible.

## ✨ Features

  - **Lean Design**: All necessary functions are in a single, lightweight file.
  - **Easy Integration**: Simply copy the library file into your project and get started.
  - **Raspberry Pi 5 Compatible**: Uses the modern `gpiod` library instead of the deprecated `RPi.GPIO`.
  - **SPI Focused**: Optimized for stable and fast SPI communication.
  - **Clear Example Code**: Includes a ready-to-run example for reading card UIDs.

## 📋 Requirements

### Hardware

  - Raspberry Pi 5 (or Pi 4)
  - RC522 RFID Reader Module
  - RFID Cards or Tags (e.g., MIFARE Classic 1K)
  - Jumper Wires

### Software

  - Raspberry Pi OS (Debian Bookworm or newer)
  - Python 3.8+
  - Enabled SPI interface

## 🔌 Hardware Wiring (SPI)

Connect your RC522 module to your Raspberry Pi's GPIO pins as follows:

| RC522 Pin  | Pi 5 Pin (Physical) | GPIO (BCM) | Description            |
| :--------- | :------------------ | :--------- | :--------------------- |
| **SDA/SS** | Pin 24              | GPIO 8     | Chip Select (CS)       |
| **SCK** | Pin 23              | GPIO 11    | SPI Clock              |
| **MOSI** | Pin 19              | GPIO 10    | Master Out -\> Slave In |
| **MISO** | Pin 21              | GPIO 9     | Master In \<- Slave Out |
| **RST** | Pin 15              | GPIO 22    | Reset                  |
| **GND** | Pin 6, 9, etc.      | -          | Ground                 |
| **VCC** | Pin 2 or 4          | -          | 3.3V Power             |

**Important:** Only connect the RC522 to a **3.3V pin**, never to 5V, as this can damage the module\!

## 🚀 Installation & Setup

### 1\. Enable SPI Interface

If you haven't already, enable the SPI interface on your Raspberry Pi:

```bash
sudo raspi-config
```

Navigate to `3 Interface Options` -\> `I4 SPI` and enable the interface.

### 2\. Install System Dependencies

Open a terminal and install the necessary Python libraries:

```bash
sudo apt update
sudo apt install python3-spidev python3-libgpiod -y
```

### 3\. Download Project Files

Download the two files below into a new project directory on your Raspberry Pi (or create them by copying and pasting the code).

**a) The Library File: `rc522_spi_library.py`**

This is the actual library.

\<details\>
\<summary\>▶️ Show Code for rc522\_spi\_library.py\</summary\>

```python
# -*- coding: utf-8 -*-
#
# A lean Python library for the RC522 RFID reader on the Raspberry Pi 5 via SPI.
#
import time
import logging

try:
    import gpiod
    import spidev
except ImportError:
    print("Important Note: The hardware libraries 'gpiod' and 'spidev' could not be imported.")
    print("This library is intended for use on a Raspberry Pi with the SPI interface enabled.")
    gpiod = None
    spidev = None

# --- Constants ---
class RC522Registers:
    COMMAND_REG = 0x01; COM_IRQ_REG = 0x04; DIV_IRQ_REG = 0x05; ERROR_REG = 0x06
    STATUS2_REG = 0x08; FIFO_DATA_REG = 0x09; FIFO_LEVEL_REG = 0x0A; CONTROL_REG = 0x0C
    BIT_FRAMING_REG = 0x0D; TX_CONTROL_REG = 0x14; VERSION_REG = 0x37; T_MODE_REG = 0x2A
    T_PRESCALER_REG = 0x2B; T_RELOAD_REG_H = 0x2C; T_RELOAD_REG_L = 0x2D; MODE_REG = 0x11
    TX_AUTO_REG = 0x15

class RC522Commands:
    IDLE = 0x00; CALC_CRC = 0x03; TRANSCEIVE = 0x0C; MF_AUTHENT = 0x0E; SOFT_RESET = 0x0F

class MifareCommands:
    REQUEST_A = 0x26; ANTICOLL_1 = 0x93

class StatusCodes:
    OK = 0; ERROR = 1; TIMEOUT = 3

# --- Exceptions ---
class RC522Error(Exception):
    """Base exception for RC522 operations."""
    pass

class RC522CommunicationError(RC522Error):
    """Exception for communication errors with the RC522."""
    pass

# --- Main Class ---
class RC522SPILibrary:
    def __init__(self, spi_bus=0, spi_device=0, rst_pin=22):
        if not spidev or not gpiod:
            raise RC522CommunicationError("Hardware libraries are not available.")
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0
        try:
            self.gpio_chip = gpiod.Chip('gpiochip4')
            self.rst_line = self.gpio_chip.get_line(rst_pin)
            self.rst_line.request(consumer="RC522_RST", type=gpiod.LINE_REQ_DIR_OUT)
        except Exception as e:
            raise RC522CommunicationError(f"Error during GPIO setup: {e}")
        self._initialized = False
        self.initialize()
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): self.cleanup()
    def _write_register(self, reg, value): self.spi.xfer2([reg << 1 & 0x7E, value])
    def _read_register(self, reg): return self.spi.xfer2([(reg << 1 & 0x7E) | 0x80, 0])[1]
    def _set_bit_mask(self, reg, mask): self._write_register(reg, self._read_register(reg) | mask)
    def _reset(self):
        self.rst_line.set_value(0); time.sleep(0.05)
        self.rst_line.set_value(1); time.sleep(0.05)
    def initialize(self):
        self._reset()
        self._write_register(RC522Registers.COMMAND_REG, RC522Commands.SOFT_RESET); time.sleep(0.05)
        self._write_register(RC522Registers.T_MODE_REG, 0x8D)
        self._write_register(RC522Registers.T_PRESCALER_REG, 0x3E)
        self._write_register(RC522Registers.T_RELOAD_REG_L, 30)
        self._write_register(RC522Registers.T_RELOAD_REG_H, 0)
        self._write_register(RC522Registers.TX_AUTO_REG, 0x40)
        self._write_register(RC522Registers.MODE_REG, 0x3D)
        if not (self._read_register(RC522Registers.TX_CONTROL_REG) & 0x03):
            self._set_bit_mask(RC522Registers.TX_CONTROL_REG, 0x03)
        self._initialized = True
    def cleanup(self):
        if self._initialized: self._reset()
        if hasattr(self, 'rst_line') and self.rst_line: self.rst_line.release()
        if hasattr(self, 'gpio_chip') and self.gpio_chip: self.gpio_chip.close()
        self.spi.close()
    def _communicate_with_card(self, command, send_data, timeout=0.1):
        self._write_register(RC522Registers.COMMAND_REG, RC522Commands.IDLE)
        self._write_register(RC522Registers.COM_IRQ_REG, 0x7F)
        self._write_register(RC522Registers.FIFO_LEVEL_REG, self._read_register(RC522Registers.FIFO_LEVEL_REG) | 0x80)
        for byte in send_data: self._write_register(RC522Registers.FIFO_DATA_REG, byte)
        self._write_register(RC522Registers.COMMAND_REG, command)
        if command == RC522Commands.TRANSCEIVE: self._set_bit_mask(RC522Registers.BIT_FRAMING_REG, 0x80)
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._read_register(RC522Registers.COM_IRQ_REG) & 0x30: break
        self._write_register(RC522Registers.BIT_FRAMING_REG, self._read_register(RC522Registers.BIT_FRAMING_REG) & ~0x80)
        if time.time() - start_time >= timeout: return StatusCodes.TIMEOUT, [], 0
        if self._read_register(RC522Registers.ERROR_REG) & 0x1B: return StatusCodes.ERROR, [], 0
        if command != RC522Commands.TRANSCEIVE: return StatusCodes.OK, [], 0
        fifo_size = self._read_register(RC522Registers.FIFO_LEVEL_REG)
        back_data = [self._read_register(RC522Registers.FIFO_DATA_REG) for _ in range(fifo_size)]
        return StatusCodes.OK, back_data, 0
    def request(self):
        self._write_register(RC522Registers.BIT_FRAMING_REG, 0x07)
        status, _, _ = self._communicate_with_card(RC522Commands.TRANSCEIVE, [MifareCommands.REQUEST_A])
        return (status, None) if status != StatusCodes.OK else (StatusCodes.OK, True)
    def anticoll(self):
        self._write_register(RC522Registers.BIT_FRAMING_REG, 0x00)
        status, back_data, _ = self._communicate_with_card(RC522Commands.TRANSCEIVE, [MifareCommands.ANTICOLL_1, 0x20])
        if status == StatusCodes.OK and len(back_data) == 5:
            # A basic checksum check
            if sum(back_data[:4]) % 256 == back_data[4]:
                return StatusCodes.OK, back_data[:4]
        return StatusCodes.ERROR, None
```

\</details\>

**b) The Example File: `card_reader_example.py`**

This script imports the library and shows how to read a card's UID.

```python
# -*- coding: utf-8 -*-

import time
import logging
from rc522_spi_library import RC522SPILibrary, StatusCodes

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    General example for reading the UID from any RFID card.
    """
    print("Starting the RFID Card Reader...")
    print("Hold any RFID card near the reader.")
    print("Press CTRL+C to exit.")

    reader = None
    try:
        reader = RC522SPILibrary(rst_pin=22)
        last_uid = None

        while True:
            status, _ = reader.request()
            if status == StatusCodes.OK:
                status, uid = reader.anticoll()
                if status == StatusCodes.OK and uid != last_uid:
                    last_uid = uid
                    uid_str = ":".join([f"{i:02X}" for i in uid])
                    print("\n================================")
                    print(f"Card detected! UID: {uid_str}")
                    print("================================")
            else:
                if last_uid is not None:
                    print("\nCard removed.")
                    last_uid = None
            time.sleep(0.1)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    except KeyboardInterrupt:
        print("\nExiting program.")
    finally:
        if reader:
            reader.cleanup()
            print("Resources released.")

if __name__ == '__main__':
    main()
```

## 💡 Usage

In your terminal, navigate to the folder where you saved the two files and run the example script:

```bash
python3 card_reader_example.py
```

Now, when you hold an RFID card near the reader, its UID should appear on the screen. You can copy this UID and use it in your own projects for access control, identification, or triggering actions.

## 🤝 Contributing

Contributions are welcome\! If you find any bugs or have improvements, please feel free to create an Issue or a Pull Request in this repository.

## 📄 License

This project is licensed under the [MIT License](https://www.google.com/search?q=LICENSE).
