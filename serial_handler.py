import threading
import time
import serial
from serial.tools import list_ports


class SerialHandler:

  def __init__(self, receive_callback):
    self.serial_port = None
    self.receive_callback = receive_callback
    self.is_running = False
    self.read_thread = None

  @staticmethod
  def get_available_ports():
    """Returns a list of available serial port names."""
    ports = list_ports.comports()
    return [port.device for port in ports]

  def is_connected(self):
    """Returns True if serial port is currently open."""
    return self.serial_port is not None and self.serial_port.is_open

  def connect(self, port, baudrate=115200):
    """Connects to the selected serial port and starts listening thread."""
    try:
      self.serial_port = serial.Serial(port, baudrate, timeout=0.1)
      time.sleep(2)  # Allow ESP32 reboot/settle
      self.is_running = True
      self.read_thread = threading.Thread(target=self._read_loop, daemon=True)
      self.read_thread.start()
      return True
    except Exception as e:
      print(f"Connection error: {e}")
      return False

  def disconnect(self):
    """Closes the serial connection."""
    self.is_running = False
    if self.serial_port and self.serial_port.is_open:
      self.serial_port.close()
    self.serial_port = None

  def send(self, message):
    """Sends a string message to the ESP32 followed by a newline."""
    if self.serial_port and self.serial_port.is_open:
      try:
        self.serial_port.write((message + "\n").encode("utf-8"))
        return True
      except Exception as e:
        print(f"Write error: {e}")
        return False
    return False

  def _read_loop(self):
    """Background thread to read incoming serial data from ESP32."""
    while self.is_running and self.serial_port and self.serial_port.is_open:
      try:
        if self.serial_port.in_waiting > 0:
          line = (
              self.serial_port.readline().decode("utf-8", errors="ignore").strip()
          )
          if line:
            self.receive_callback(line)
        else:
          time.sleep(0.05)
      except Exception:
        break