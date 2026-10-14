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
