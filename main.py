<<<<<<< HEAD
import queue
import threading
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox

from modbus_handler import ModbusHandler
from serial_handler import SerialHandler
from ui_components import ModeSelectUI, ModbusUI, StyleManager, UartUI


class MainApp:
    """Main application orchestrator supporting UART Serial Monitor and Modbus Studio."""

    def __init__(self, root):
        self.root = root
        self.root.title("Communication Studio - UART & MODBUS Diagnostic Tool")
        self.root.geometry("980x660")
        self.root.minsize(820, 520)

        # Thread-safe UI event queue
        self.ui_queue = queue.Queue()
        self._is_closing = False
        self._process_ui_queue()

        # Apply cohesive dark theme styles
        StyleManager.apply(self.root)

        # Root layout scaling
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # --- Handlers ---
        self.serial_handler = SerialHandler(receive_callback=self.on_uart_received)
        self.modbus_handler = ModbusHandler(log_callback=self.on_modbus_log)

        # --- UI Views ---
        self.mode_select_ui = ModeSelectUI(
            self.root,
            on_select_uart=self.show_uart,
            on_select_modbus=self.show_modbus,
        )

        self.uart_ui = UartUI(
            self.root,
            on_back=self.show_mode_select,
            on_connect_toggle=self.toggle_uart_connection,
            on_send=self.send_uart_message,
            on_refresh_ports=self.refresh_uart_ports,
            on_clear_sent=lambda: self.uart_ui.clear_log(self.uart_ui.sent_text),
            on_clear_recv=lambda: self.uart_ui.clear_log(self.uart_ui.recv_text),
            on_save_logs=self.save_uart_logs,
        )

        self.modbus_ui = ModbusUI(
            self.root,
            on_back=self.show_mode_select,
            on_connect_toggle=self.toggle_modbus_connection,
            on_execute=self.execute_modbus_request,
            on_toggle_poll=self.toggle_modbus_poll,
            on_clear_table=lambda: self.modbus_ui.clear_table(),
            on_clear_log=lambda: self.modbus_ui.clear_log(),
            on_save_logs=self.save_modbus_logs,
        )

        # Keyboard shortcut for UART send
        self.uart_ui.entry_box.bind("<Return>", lambda _e: self.send_uart_message())

        # Start with Mode Selection Screen
        self.current_frame = None
        self.show_mode_select()

    def _process_ui_queue(self):
        """Processes events queued from background threads on the Tk main thread."""
        while not self.ui_queue.empty():
            try:
                fn = self.ui_queue.get_nowait()
                fn()
            except queue.Empty:
                break
            except Exception as exc:
                print(f"Error handling UI event: {exc}")
        if not self._is_closing:
            self.root.after(30, self._process_ui_queue)

    def post_to_ui(self, fn):
        """Safely enqueues a callable to be run on the main UI thread."""
        self.ui_queue.put(fn)

    # ==========================================
    # Navigation / View Switching
    # ==========================================

    def _switch_view(self, target_frame):
        """Hides current view and shows target view frame."""
        if self.current_frame:
            self.current_frame.grid_forget()
        self.current_frame = target_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def show_mode_select(self):
        """Displays initial mode selection screen."""
        self._switch_view(self.mode_select_ui.frame)

    def show_uart(self):
        """Displays UART Serial Monitor view."""
        self._switch_view(self.uart_ui.frame)
        self.refresh_uart_ports()

    def show_modbus(self):
        """Displays Modbus Studio view."""
        self._switch_view(self.modbus_ui.frame)
        if not ModbusHandler.is_library_available():
            messagebox.showwarning(
                "Missing Dependency",
                "The 'pymodbus' library is not detected in your Python environment.\n\n"
                "To enable Modbus functionality, install it using:\n"
                "pip install -r requirements.txt",
            )

    # ==========================================
    # UART Serial Monitor Logic
    # ==========================================

    def refresh_uart_ports(self):
        """Scans and updates available serial ports dropdown."""
        ports = SerialHandler.get_available_ports()
        self.uart_ui.port_combobox["values"] = ports
        if ports:
            self.uart_ui.port_combobox.current(0)
        else:
            self.uart_ui.port_combobox.set("")

    def toggle_uart_connection(self):
        """Connects or disconnects the serial port."""
        if not self.serial_handler.is_connected():
            port = self.uart_ui.port_combobox.get()
            baud_str = self.uart_ui.baud_combobox.get()

            if not port:
                messagebox.showerror("Error", "Please select a serial port first!")
                return

            try:
                baudrate = int(baud_str)
            except ValueError:
                baudrate = 115200

            success = self.serial_handler.connect(port, baudrate=baudrate)
            if success:
                self.uart_ui.connect_btn.config(text="Disconnect", style="Danger.TButton")
                self.uart_ui.port_combobox.config(state=tk.DISABLED)
                self.uart_ui.baud_combobox.config(state=tk.DISABLED)
                self.uart_ui.refresh_btn.config(state=tk.DISABLED)
                self.uart_ui.send_btn.config(state=tk.NORMAL)
                self.uart_ui.set_status("Connected", True)
                self.uart_ui.append_log(
                    self.uart_ui.sent_text,
                    f"[System] Connected to {port} @ {baudrate} baud",
                    tag="system",
                )
            else:
                messagebox.showerror("Connection Error", f"Failed to connect to {port}")
        else:
            self.serial_handler.disconnect()
            self.uart_ui.connect_btn.config(text="Connect", style="Success.TButton")
            self.uart_ui.port_combobox.config(state="readonly")
            self.uart_ui.baud_combobox.config(state="readonly")
            self.uart_ui.refresh_btn.config(state=tk.NORMAL)
            self.uart_ui.send_btn.config(state=tk.DISABLED)
            self.uart_ui.set_status("Disconnected", False)
            self.uart_ui.append_log(self.uart_ui.sent_text, "[System] Disconnected.", tag="system")

    def send_uart_message(self):
        """Sends user text over USB serial connection."""
        message = self.uart_ui.entry_box.get().strip()
        if not message:
            return

        success = self.serial_handler.send(message)
        if success:
            self.uart_ui.append_log(self.uart_ui.sent_text, f"> {message}", tag="tx")
            self.uart_ui.entry_box.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to send message over serial.")

    def on_uart_received(self, data):
        """Callback triggered from background serial read thread."""
        self.post_to_ui(lambda: self.uart_ui.append_log(self.uart_ui.recv_text, f"< {data}", tag="rx"))

    def save_uart_logs(self):
        """Exports UART sent and received logs to a text file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save UART Logs",
        )
        if not file_path:
            return

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sent_log = self.uart_ui.get_log_text(self.uart_ui.sent_text)
            recv_log = self.uart_ui.get_log_text(self.uart_ui.recv_text)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"=== UART SERIAL MONITOR LOG: {timestamp} ===\n\n")
                f.write("--- SENT LOG ---\n")
                f.write(sent_log + ("\n" if sent_log else ""))
                f.write("\n\n--- RECEIVED LOG ---\n")
                f.write(recv_log + ("\n" if recv_log else ""))
            messagebox.showinfo("Saved", f"UART logs saved to:\n{file_path}")
        except Exception as exc:
            messagebox.showerror("Save Error", f"Could not save logs: {exc}")

    # ==========================================
    # MODBUS Logic (TCP & Polling)
    # ==========================================

    def toggle_modbus_connection(self):
        """Connects or disconnects the Modbus TCP client."""
        if not self.modbus_handler.is_connected():
            host = self.modbus_ui.ip_entry.get().strip()
            port = self.modbus_ui.port_entry.get().strip()
            timeout = self.modbus_ui.timeout_entry.get().strip()

            if not host:
                messagebox.showerror("Error", "Please specify the ESP32 IP address!")
                return

            # Run connection attempt in background thread to avoid freezing GUI
            self.modbus_ui.set_status("Connecting...", False)
            self.modbus_ui.connect_btn.config(state=tk.DISABLED)

            def _connect_worker():
                success, err = self.modbus_handler.connect(host=host, port=port, timeout=timeout)
                self.post_to_ui(lambda: self._after_modbus_connect(success, err, host, port))

            threading.Thread(target=_connect_worker, daemon=True).start()
        else:
            self.modbus_ui.poll_var.set(False)
            self.modbus_handler.stop_polling()
            self.modbus_handler.disconnect()
            self._update_modbus_ui_disconnected()

    def _after_modbus_connect(self, success, err, host, port):
        """Updates UI after connection attempt finishes."""
        self.modbus_ui.connect_btn.config(state=tk.NORMAL)
        if success:
            self.modbus_ui.connect_btn.config(text="Disconnect", style="Danger.TButton")
            self.modbus_ui.ip_entry.config(state=tk.DISABLED)
            self.modbus_ui.port_entry.config(state=tk.DISABLED)
            self.modbus_ui.timeout_entry.config(state=tk.DISABLED)
            self.modbus_ui.exec_btn.config(state=tk.NORMAL)
            self.modbus_ui.poll_check.config(state=tk.NORMAL)
            self.modbus_ui.set_status(f"Connected ({host}:{port})", True)
        else:
            self._update_modbus_ui_disconnected()
            messagebox.showerror("Connection Error", f"Could not connect to Modbus TCP server:\n{err}")

    def _update_modbus_ui_disconnected(self):
        """Resets Modbus UI to disconnected state."""
        self.modbus_ui.connect_btn.config(text="Connect", style="Success.TButton")
        self.modbus_ui.ip_entry.config(state=tk.NORMAL)
        self.modbus_ui.port_entry.config(state=tk.NORMAL)
        self.modbus_ui.timeout_entry.config(state=tk.NORMAL)
        self.modbus_ui.exec_btn.config(state=tk.DISABLED)
        self.modbus_ui.poll_check.config(state=tk.DISABLED)
        self.modbus_ui.set_status("Disconnected", False)

    def _parse_modbus_request_params(self):
        """Extracts and validates input parameters for a Modbus request."""
        func_str = self.modbus_ui.func_combobox.get()
        func_code = int(func_str.split(":")[0])
        addr = int(self.modbus_ui.addr_entry.get().strip() or 0)
        unit_id = int(self.modbus_ui.unit_entry.get().strip() or 1)
        count = int(self.modbus_ui.count_entry.get().strip() or 1)

        values = None
        raw_val = self.modbus_ui.value_entry.get().strip()
        if func_code in (5, 6, 15, 16):
            if not raw_val:
                raise ValueError("Please provide a value in the Value(s) field for write requests.")

            if func_code == 5:  # Single coil
                val = 1 if raw_val in ("1", "true", "True", "on", "ON") else 0
                values = [val]
            elif func_code == 6:  # Single register
                values = [int(raw_val, 0)]
            elif func_code == 15:  # Multiple coils
                values = [1 if x.strip() in ("1", "true", "True", "on", "ON") else 0 for x in raw_val.split(",")]
            elif func_code == 16:  # Multiple registers
                values = [int(x.strip(), 0) for x in raw_val.split(",") if x.strip()]

        return {
            "function_code": func_code,
            "address": addr,
            "count": count,
            "values": values,
            "unit_id": unit_id,
        }

    def execute_modbus_request(self):
        """Executes a single Modbus operation in background thread."""
        try:
            params = self._parse_modbus_request_params()
        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))
            return

        def _worker():
            result = self.modbus_handler.execute_function(**params)
            self.post_to_ui(lambda: self._handle_modbus_result(result))

        threading.Thread(target=_worker, daemon=True).start()

    def _handle_modbus_result(self, result):
        """Updates table grid when data is received."""
        if result.get("success") and "values" in result:
            reg_type = result.get("type", "Register")
            start_addr = result.get("address", 0)
            values = result.get("values", [])
            self.modbus_ui.update_table_data(reg_type, start_addr, values)

    def toggle_modbus_poll(self):
        """Toggles background periodic auto-polling."""
        if self.modbus_ui.poll_var.get():
            try:
                params = self._parse_modbus_request_params()
            except ValueError as exc:
                self.modbus_ui.poll_var.set(False)
                messagebox.showerror("Polling Error", f"Invalid parameters for auto-polling:\n{exc}")
                return

            if params["function_code"] not in (1, 2, 3, 4):
                self.modbus_ui.poll_var.set(False)
                messagebox.showwarning("Notice", "Auto-polling is only supported for Read functions (FC 01-04).")
                return

            interval_str = self.modbus_ui.poll_interval_combo.get().replace(" ms", "").strip()
            interval_sec = float(interval_str) / 1000.0

            ok, err = self.modbus_handler.start_polling(
                poll_params=params,
                interval_seconds=interval_sec,
                callback=lambda res: self.post_to_ui(lambda: self._handle_modbus_result(res)),
            )
            if not ok:
                self.modbus_ui.poll_var.set(False)
                messagebox.showerror("Error", err)
        else:
            self.modbus_handler.stop_polling()

    def on_modbus_log(self, message, tag):
        """Thread-safe callback to append transaction messages in Modbus terminal."""
        self.post_to_ui(lambda: self.modbus_ui.append_log(message, tag=tag))

    def save_modbus_logs(self):
        """Exports Modbus data table and communication log to text file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Modbus Session Logs",
        )
        if not file_path:
            return

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_text = self.modbus_ui.get_log_text()

            # Gather treeview rows
            rows = []
            for child in self.modbus_ui.tree.get_children():
                vals = self.modbus_ui.tree.item(child)["values"]
                rows.append(" | ".join(str(v) for v in vals))

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"=== MODBUS STUDIO SESSION LOG: {timestamp} ===\n\n")
                f.write("--- CURRENT REGISTER / COIL TABLE ---\n")
                f.write("Address | Type | Dec | Hex | Binary/State | Updated\n")
                f.write("-" * 65 + "\n")
                if rows:
                    f.write("\n".join(rows) + "\n")
                else:
                    f.write("(No register values logged)\n")
                f.write("\n\n--- TRANSACTION LOG ---\n")
                f.write(log_text + ("\n" if log_text else ""))
            messagebox.showinfo("Saved", f"Modbus logs saved to:\n{file_path}")
        except Exception as exc:
            messagebox.showerror("Save Error", f"Could not save logs: {exc}")

    # ==========================================
    # Teardown
    # ==========================================

    def on_close(self):
        """Cleans up serial, Modbus connections and background threads on exit."""
        self._is_closing = True
        try:
            if self.serial_handler:
                self.serial_handler.disconnect()
            if self.modbus_handler:
                self.modbus_handler.disconnect()
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
=======
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox
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
        on_save_logs=self.save_logs,
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
        self.ui.set_status("Connected", True)
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
      self.ui.set_status("Disconnected", False)
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

  def save_logs(self):
    """Export the current sent and received logs to a text file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Save serial logs",
    )
    if not file_path:
      return

    try:
      timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      sent_log = self.ui.get_log_text(self.ui.sent_text)
      recv_log = self.ui.get_log_text(self.ui.recv_text)
      with open(file_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"Serial monitor log saved: {timestamp}\n\n")
        log_file.write("--- SENT LOG ---\n")
        log_file.write(sent_log + ("\n" if sent_log else ""))
        log_file.write("\n\n--- RECEIVED LOG ---\n")
        log_file.write(recv_log + ("\n" if recv_log else ""))
      messagebox.showinfo("Saved", f"Logs saved to:\n{file_path}")
    except Exception as exc:  # pragma: no cover - GUI error path
      messagebox.showerror("Save Error", f"Could not save logs: {exc}")

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
>>>>>>> 5154e379dacb7e6037c2f38987144453a81a3724
