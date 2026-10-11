import tkinter as tk
from tkinter import messagebox
from serial_handler import SerialHandler
from ui_components import AppUI


class MainApp:

  def __init__(self, root):
    self.root = root
    self.is_connected = False

    # Initialize serial handler with callback for received data
    self.serial_handler = SerialHandler(receive_callback=self.on_data_received)

    # Initialize UI and pass clear log callbacks
    self.ui = AppUI(
        root,
        on_connect_toggle=self.toggle_connection,
        on_send=self.send_message,
        on_refresh_ports=self.refresh_ports,
        on_clear_sent=lambda: self.ui.clear_log(self.ui.sent_text),
        on_clear_recv=lambda: self.ui.clear_log(self.ui.recv_text),
    )

    # Populate ports on startup
    self.refresh_ports()

    # Bind Enter key to send
    self.ui.entry_box.bind("<Return>", lambda event: self.send_message())

  def refresh_ports(self):
    """Scans and updates the dropdown list of serial ports."""
    ports = SerialHandler.get_available_ports()
    self.ui.port_combobox["values"] = ports
    if ports:
      self.ui.port_combobox.current(0)
    else:
      self.ui.port_combobox.set("")

  def toggle_connection(self):
    """Handles connecting and disconnecting using selected port and baudrate."""
    if not self.is_connected:
      selected_port = self.ui.port_combobox.get()
      selected_baud = self.ui.baud_combobox.get()

      if not selected_port:
        messagebox.showerror("Error", "Please select a serial port first!")
        return

      try:
        baudrate = int(selected_baud)
      except ValueError:
        baudrate = 115200

      success = self.serial_handler.connect(selected_port, baudrate=baudrate)
      if success:
        self.is_connected = True
        self.ui.connect_btn.config(text="Disconnect")
        self.ui.port_combobox.config(state=tk.DISABLED)
        self.ui.baud_combobox.config(state=tk.DISABLED)
        self.ui.refresh_btn.config(state=tk.DISABLED)
        self.ui.send_btn.config(state=tk.NORMAL)
        self.ui.append_log(
            self.ui.sent_text,
            f"[System] Connected to {selected_port} at {baudrate} baud",
        )
      else:
        messagebox.showerror(
            "Connection Error", f"Failed to connect to {selected_port}"
        )
    else:
      self.serial_handler.disconnect()
      self.is_connected = False
      self.ui.connect_btn.config(text="Connect")
      self.ui.port_combobox.config(state="readonly")
      self.ui.baud_combobox.config(state="readonly")
      self.ui.refresh_btn.config(state=tk.NORMAL)
      self.ui.send_btn.config(state=tk.DISABLED)
      self.ui.append_log(self.ui.sent_text, "[System] Disconnected.")

  def send_message(self):
    """Sends text from input field to ESP32 and updates the sent log terminal."""
    message = self.ui.entry_box.get().strip()
    if not message:
      return

    success = self.serial_handler.send(message)
    if success:
      self.ui.append_log(self.ui.sent_text, f"> {message}")
      self.ui.entry_box.delete(0, tk.END)
    else:
      messagebox.showerror("Error", "Failed to send message over serial.")

  def on_data_received(self, data):
    """Thread-safe callback triggered when data comes back from the ESP32."""
    self.root.after(0, lambda: self.ui.append_log(self.ui.recv_text, f"< {data}"))

  def on_close(self):
    """Clean up resources on application exit."""
    self.serial_handler.disconnect()
    self.root.destroy()


if __name__ == "__main__":
  root = tk.Tk()
  app = MainApp(root)
  root.protocol("WM_DELETE_WINDOW", app.on_close)
  root.mainloop()