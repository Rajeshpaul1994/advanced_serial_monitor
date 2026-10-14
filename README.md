<<<<<<< HEAD
# Communication Studio - UART & MODBUS Diagnostic Tool

A modern desktop application built with Python, Tkinter, pySerial, and pymodbus. It provides a unified launcher allowing you to select between **UART Serial Monitor** (USB serial communication) and **MODBUS Studio** (Modbus TCP client over WiFi/LAN).

---

## Features

### 1. Launcher / Mode Selector
- Interactive startup screen allowing you to choose between **UART** and **MODBUS**.
- Seamless navigation: switch back to mode selection anytime using the `⬅ Back to Modes` button.

### 2. UART Serial Monitor
- Auto-scan serial/COM ports with one-click refresh.
- Configurable baud rates (9600 to 921600, default `115200`).
- Non-blocking background receiver thread.
- Dual terminal console: dedicated **Sent Log** (amber) and **Received Log** (matrix phosphor green) with clear buttons.
- Export communication logs to `.txt` files.

### 3. MODBUS Studio
- **Protocol Selection**: Switch between **MODBUS TCP** (Active) and **MODBUS RTU** (Serial placeholder).
- **Modbus TCP Client**:
  - Connect to your **ESP32**, Arduino, or PLC over WiFi or local network.
  - Configurable IP, Port (default `502`), Unit ID, and Timeout.
  - Supports standard Function Codes:
    - `FC 01`: Read Coils
    - `FC 02`: Read Discrete Inputs
    - `FC 03`: Read Holding Registers
    - `FC 04`: Read Input Registers
    - `FC 05`: Write Single Coil (1 / 0)
    - `FC 06`: Write Single Register (0 - 65535)
    - `FC 15`: Write Multiple Coils (e.g. `1, 0, 1`)
    - `FC 16`: Write Multiple Registers (e.g. `100, 200, 300`)
  - **Live Register View**: Real-time table displaying Address, Register Type, Decimal, Hex (`0x...`), Binary/State, and Last Updated timestamp.
  - **Transaction Terminal**: Detailed frame log showing TX requests, RX responses, and Modbus exceptions.
  - **Auto-Polling**: Continuous periodic reading (500ms, 1000ms, 2000ms, 5000ms) to monitor live ESP32 sensors.
  - **Save Logs**: Export both the register table snapshot and transaction history.

---

## Requirements

- Python 3.9+
- Tkinter (`python3-tk` on Debian/Ubuntu Linux)
- Python packages:
  - `pyserial>=3.5,<4.0`
  - `pymodbus>=3.5.0`

---

## Installation & Running

### Linux (Ubuntu/Debian)

```bash
# 1. Install system requirements
sudo apt update
sudo apt install python3 python3-venv python3-tk

# 2. Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Start the application
python main.py
```

### Windows (PowerShell)

```powershell
# 1. Create and activate virtual environment
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
python -m pip install -r requirements.txt

# 3. Start the application
python main.py
```

---

## Testing MODBUS TCP with ESP32 over WiFi

A complete, ready-to-flash ESP32 Arduino sketch is included in:
[`examples/esp32_modbus_tcp/esp32_modbus_tcp.ino`](examples/esp32_modbus_tcp/esp32_modbus_tcp.ino)

### Steps to test:
1. Open the Arduino IDE.
2. Go to **Tools -> Manage Libraries**, search for `ModbusIP_ESP8266` by André Sarmento, and install it.
3. Open `examples/esp32_modbus_tcp/esp32_modbus_tcp.ino` and enter your WiFi credentials (`ssid` & `password`).
4. Upload to your ESP32 and open the Arduino Serial Monitor at `115200` baud.
5. Note the IP address printed by the ESP32 (e.g., `192.168.1.105`).
6. Launch **Communication Studio**:
   - Click **Launch MODBUS Studio**.
   - Ensure **MODBUS TCP** is selected.
   - Enter your ESP32's IP address in the **ESP32 IP** field (Port: `502`, Unit ID: `1`).
   - Click **Connect**.
   - Select `03: Read Holding Registers (FC 03)`, set Address `0`, Count `3`, and click **Execute Request** (or enable **Auto-Poll**).
   - Test writing: Select `05: Write Single Coil (FC 05)`, Address `0`, Value `1` -> Your ESP32's onboard LED turns ON! Set Value `0` -> LED turns OFF.

---

## Building Executables (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --clean --noconfirm AdvancedSerialMonitor.spec
```
The standalone binary will be generated in `dist/AdvancedSerialMonitor` (or `.exe` on Windows).
=======
# Advanced Serial Monitor

A desktop serial monitor built with Python, Tkinter, and pySerial. It lets you
connect to a serial port, send messages, view sent and received data, and save
the logs to a text file.

<img width="853" height="540" alt="image" src="https://github.com/user-attachments/assets/b939f46a-e99b-4b50-a38f-d49bbe99ced4" />


## Requirements

- Python 3
- Tkinter (usually included with Python on Windows; on Linux, install your
  distribution's Tk package if it is missing)
- A serial device, such as an ESP32, and a USB cable/serial adapter

## Install and run from source

### Windows

1. Install Python 3 from [python.org](https://www.python.org/downloads/). Enable
   **Add Python to PATH** in the installer.
2. Open PowerShell in the project directory and create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run
   `.\.venv\Scripts\activate.bat` instead.
3. Install the Python dependency and start the app:

   ```powershell
   python -m pip install -r requirements.txt
   python main.py
   ```

### Linux

1. Install Python 3, `venv`, and Tkinter using your distribution's package
   manager. On Debian or Ubuntu:

   ```bash
   sudo apt update
   sudo apt install python3 python3-venv python3-tk
   ```

2. From the project directory, create and activate a virtual environment,
   install the dependency, and run the app:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   python main.py
   ```

## Using the app

1. Connect your serial device to the computer.
2. Click **Refresh** to scan for available serial ports, then select the
   device's port.
3. Choose the baud rate configured on the device. The default is `115200`.
4. Click **Connect**. The status indicator shows whether the connection is
   active.
5. Enter a message in the input field and click **Send** (or press Enter).
   Messages are sent as UTF-8 text followed by a newline.
6. Review the **Sent Log** and **Received Log**. Use each **Clear** button to
   clear that log.
7. Click **Save Logs** to export both logs to a `.txt` file.
8. Click **Disconnect** before unplugging the device or when finished.

## Linux serial-port permissions

If the app cannot open a port due to permissions, your Linux distribution may
require your user to belong to the serial-port group, commonly `dialout` on
Debian/Ubuntu:

```bash
sudo usermod -aG dialout "$USER"
```

Log out and back in for the group change to take effect. The group name and
permissions can differ between Linux distributions.

## Build downloadable executables

PyInstaller builds should be made on the target operating system; a Windows
build produces a Windows executable, and a Linux build produces a Linux
executable. Install PyInstaller in the activated virtual environment:

```bash
python -m pip install pyinstaller
```

Then run the appropriate command from the project directory.

**Windows (PowerShell):**

```powershell
pyinstaller --clean --noconfirm --onefile --windowed --name AdvancedSerialMonitor main.py
```

The executable is written to `dist\AdvancedSerialMonitor.exe`.

**Linux:**

```bash
pyinstaller --clean --noconfirm --onefile --windowed --name AdvancedSerialMonitor main.py
chmod +x dist/AdvancedSerialMonitor
```

The executable is written to `dist/AdvancedSerialMonitor`. Test each build on
its target operating system before sharing it. Linux users may still need
Tk-related system libraries and serial-port permissions.
>>>>>>> 5154e379dacb7e6037c2f38987144453a81a3724
