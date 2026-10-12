# Advanced Serial Monitor

A desktop serial monitor built with Python, Tkinter, and pySerial. It lets you
connect to a serial port, send messages, view sent and received data, and save
the logs to a text file.

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
