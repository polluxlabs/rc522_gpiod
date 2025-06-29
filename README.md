
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


**b) The Example File: `example.py`**

This script imports the library and shows how to read a card's UID.


## 💡 Usage

In your terminal, navigate to the folder where you saved the two files and run the example script:

```bash
python3 example.py
```

Now, when you hold an RFID card near the reader, its UID should appear on the screen. You can copy this UID and use it in your own projects for access control, identification, or triggering actions.

## 🤝 Contributing

Contributions are welcome\! If you find any bugs or have improvements, please feel free to create an Issue or a Pull Request in this repository.

## 📄 License

This project is licensed under the [MIT License](https://www.google.com/search?q=LICENSE).
