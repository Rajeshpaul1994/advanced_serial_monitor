import threading
import time
import inspect
from datetime import datetime

try:
    from pymodbus.client import ModbusTcpClient
    from pymodbus.exceptions import ModbusException, ConnectionException
    PYMODBUS_AVAILABLE = True
except ImportError:
    ModbusTcpClient = None
    ModbusException = Exception
    ConnectionException = Exception
    PYMODBUS_AVAILABLE = False


class ModbusHandler:
    """Handles Modbus TCP client communication and auto-polling."""

    def __init__(self, log_callback=None, data_callback=None):
        self.client = None
        self.host = None
        self.port = 502
        self.log_callback = log_callback
        self.data_callback = data_callback
        self._is_connected = False

        # Polling controls
        self.poll_thread = None
        self.poll_running = False
        self.poll_interval = 1.0  # seconds
        self.poll_request_params = None

    @staticmethod
    def is_library_available():
        """Check if pymodbus is installed."""
        return PYMODBUS_AVAILABLE

    def is_connected(self):
        """Returns True if client is connected."""
        return self._is_connected and self.client is not None

    def _log(self, message, tag="info"):
        """Sends timestamped log messages to callback if present."""
        if self.log_callback:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_callback(f"[{timestamp}] {message}", tag)

    def connect(self, host, port=502, timeout=3.0):
        """Connects to Modbus TCP server (e.g. ESP32)."""
        if not PYMODBUS_AVAILABLE:
            error_msg = "pymodbus library is not installed. Run: pip install pymodbus"
            self._log(f"ERR: {error_msg}", tag="error")
            return False, error_msg

        self.disconnect()

        try:
            self.host = host.strip()
            self.port = int(port)
            self._log(f"Connecting to Modbus TCP {self.host}:{self.port} (timeout={timeout}s)...", tag="info")
            self.client = ModbusTcpClient(host=self.host, port=self.port, timeout=float(timeout))
            connected = self.client.connect()

            if connected:
                self._is_connected = True
                self._log(f"Connected to Modbus TCP server at {self.host}:{self.port}", tag="success")
                return True, ""
            else:
                self._is_connected = False
                error_msg = f"Failed to connect to {self.host}:{self.port}. Is the device reachable?"
                self._log(f"ERR: {error_msg}", tag="error")
                return False, error_msg
        except Exception as exc:
            self._is_connected = False
            error_msg = f"Connection error: {exc}"
            self._log(f"ERR: {error_msg}", tag="error")
            return False, error_msg

    def disconnect(self):
        """Disconnects client and stops auto-polling."""
        self.stop_polling()
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass
            self.client = None
        if self._is_connected:
            self._is_connected = False
            self._log("Disconnected from Modbus TCP server.", tag="warning")

    def _call_client(self, method_name, *args, unit_id=1, **kwargs):
        """
        Dynamically adapts unit_id/device_id/slave keyword arguments
        for compatibility across different pymodbus versions.
        """
        if not self.is_connected():
            raise ConnectionException("Not connected to Modbus TCP server.")

        method = getattr(self.client, method_name)
        sig = inspect.signature(method)

        if "device_id" in sig.parameters:
            kwargs["device_id"] = int(unit_id)
        elif "slave" in sig.parameters:
            kwargs["slave"] = int(unit_id)

        return method(*args, **kwargs)

    def execute_function(self, function_code, address, count=1, values=None, unit_id=1):
        """
        Executes a Modbus request based on standard function code:
        - 1: Read Coils
        - 2: Read Discrete Inputs
        - 3: Read Holding Registers
        - 4: Read Input Registers
        - 5: Write Single Coil
        - 6: Write Single Register
        - 15: Write Multiple Coils
        - 16: Write Multiple Registers
        """
        if not self.is_connected():
            return {
                "success": False,
                "error": "Not connected to Modbus TCP server.",
                "function_code": function_code,
            }

        try:
            address = int(address)
            unit_id = int(unit_id)
            func_code = int(function_code)

            if func_code == 1:  # Read Coils
                count = int(count)
                self._log(f"TX -> FC01 Read Coils | Unit: {unit_id} | Addr: {address} | Count: {count}", tag="tx")
                res = self._call_client("read_coils", address, count=count, unit_id=unit_id)
                if res.isError():
                    err_msg = f"Modbus Exception: {res}"
                    self._log(f"RX <- ERR: {err_msg}", tag="error")
                    return {"success": False, "error": err_msg, "function_code": 1}
                bits = res.bits[:count]
                self._log(f"RX <- Coils: {bits}", tag="rx")
                return {
                    "success": True,
                    "function_code": 1,
                    "type": "Coil",
                    "address": address,
                    "count": count,
                    "values": [1 if b else 0 for b in bits],
                }

            elif func_code == 2:  # Read Discrete Inputs
                count = int(count)
                self._log(f"TX -> FC02 Read Discrete Inputs | Unit: {unit_id} | Addr: {address} | Count: {count}", tag="tx")
                res = self._call_client("read_discrete_inputs", address, count=count, unit_id=unit_id)
                if res.isError():
                    err_msg = f"Modbus Exception: {res}"
                    self._log(f"RX <- ERR: {err_msg}", tag="error")
                    return {"success": False, "error": err_msg, "function_code": 2}
                bits = res.bits[:count]
                self._log(f"RX <- Discrete Inputs: {bits}", tag="rx")
                return {
                    "success": True,
                    "function_code": 2,
                    "type": "Discrete Input",
                    "address": address,
                    "count": count,
                    "values": [1 if b else 0 for b in bits],
                }

            elif func_code == 3:  # Read Holding Registers
                count = int(count)
                self._log(f"TX -> FC03 Read Holding Registers | Unit: {unit_id} | Addr: {address} | Count: {count}", tag="tx")
                res = self._call_client("read_holding_registers", address, count=count, unit_id=unit_id)
                if res.isError():
                    err_msg = f"Modbus Exception: {res}"
                    self._log(f"RX <- ERR: {err_msg}", tag="error")
                    return {"success": False, "error": err_msg, "function_code": 3}
                regs = res.registers
                self._log(f"RX <- Holding Registers: {regs}", tag="rx")
                return {
                    "success": True,
                    "function_code": 3,
                    "type": "Holding Register",
                    "address": address,
                    "count": count,
                    "values": regs,
                }

            elif func_code == 4:  # Read Input Registers
                count = int(count)
                self._log(f"TX -> FC04 Read Input Registers | Unit: {unit_id} | Addr: {address} | Count: {count}", tag="tx")
                res = self._call_client("read_input_registers", address, count=count, unit_id=unit_id)
                if res.isError():
                    err_msg = f"Modbus Exception: {res}"
                    self._log(f"RX <- ERR: {err_msg}", tag="error")
                    return {"success": False, "error": err_msg, "function_code": 4}
                regs = res.registers
                self._log(f"RX <- Input Registers: {regs}", tag="rx")
                return {
                    "success": True,
                    "function_code": 4,
                    "type": "Input Register",
                    "address": address,
                    "count": count,
                    "values": regs,
                }

            elif func_code == 5:  # Write Single Coil
                val_bool = bool(values[0] if isinstance(values, (list, tuple)) else values)
                self._log(f"TX -> FC05 Write Single Coil | Unit: {unit_id} | Addr: {address} | Value: {val_bool}", tag="tx")
                res = self._call_client("write_coil", address, val_bool, unit_id=unit_id)
                if res.isError():
                    err_msg = f"Modbus Exception: {res}"
                    self._log(f"RX <- ERR: {err_msg}", tag="error")
                    return {"success": False, "error": err_msg, "function_code": 5}
                self._log(f"RX <- Write Coil OK (Addr: {address}, Val: {val_bool})", tag="success")
                return {
                    "success": True,
                    "function_code": 5,
                    "type": "Coil",
                    "address": address,
                    "count": 1,
                    "values": [1 if val_bool else 0],
                }

            elif func_code == 6:  # Write Single Register
                reg_val = int(values[0] if isinstance(values, (list, tuple)) else values)
                self._log(f"TX -> FC06 Write Single Register | Unit: {unit_id} | Addr: {address} | Value: {reg_val}", tag="tx")
                res = self._call_client("write_register", address, reg_val, unit_id=unit_id)
                if res.isError():
                    err_msg = f"Modbus Exception: {res}"
                    self._log(f"RX <- ERR: {err_msg}", tag="error")
                    return {"success": False, "error": err_msg, "function_code": 6}
                self._log(f"RX <- Write Register OK (Addr: {address}, Val: {reg_val})", tag="success")
                return {
                    "success": True,
                    "function_code": 6,
                    "type": "Holding Register",
                    "address": address,
                    "count": 1,
                    "values": [reg_val],
                }

            elif func_code == 15:  # Write Multiple Coils
                coils_list = [bool(x) for x in (values if isinstance(values, (list, tuple)) else [values])]
                self._log(f"TX -> FC15 Write Multiple Coils | Unit: {unit_id} | Addr: {address} | Values: {coils_list}", tag="tx")
                res = self._call_client("write_coils", address, coils_list, unit_id=unit_id)
                if res.isError():
                    err_msg = f"Modbus Exception: {res}"
                    self._log(f"RX <- ERR: {err_msg}", tag="error")
                    return {"success": False, "error": err_msg, "function_code": 15}
                self._log(f"RX <- Write Multiple Coils OK ({len(coils_list)} coils written)", tag="success")
                return {
                    "success": True,
                    "function_code": 15,
                    "type": "Coil",
                    "address": address,
                    "count": len(coils_list),
                    "values": [1 if c else 0 for c in coils_list],
                }

            elif func_code == 16:  # Write Multiple Registers
                regs_list = [int(x) for x in (values if isinstance(values, (list, tuple)) else [values])]
                self._log(f"TX -> FC16 Write Multiple Registers | Unit: {unit_id} | Addr: {address} | Values: {regs_list}", tag="tx")
                res = self._call_client("write_registers", address, regs_list, unit_id=unit_id)
                if res.isError():
                    err_msg = f"Modbus Exception: {res}"
                    self._log(f"RX <- ERR: {err_msg}", tag="error")
                    return {"success": False, "error": err_msg, "function_code": 16}
                self._log(f"RX <- Write Multiple Registers OK ({len(regs_list)} registers written)", tag="success")
                return {
                    "success": True,
                    "function_code": 16,
                    "type": "Holding Register",
                    "address": address,
                    "count": len(regs_list),
                    "values": regs_list,
                }

            else:
                err_msg = f"Unsupported Function Code: {func_code}"
                self._log(f"ERR: {err_msg}", tag="error")
                return {"success": False, "error": err_msg}

        except Exception as exc:
            err_msg = f"Transaction error: {exc}"
            self._log(f"ERR: {err_msg}", tag="error")
            return {"success": False, "error": err_msg, "function_code": function_code}

    def start_polling(self, poll_params, interval_seconds=1.0, callback=None):
        """Starts background periodic polling for read requests."""
        if not self.is_connected():
            return False, "Connect to Modbus TCP server first."

        self.stop_polling()
        self.poll_request_params = poll_params
        self.poll_interval = max(0.2, float(interval_seconds))
        self.poll_running = True

        def _poll_worker():
            while self.poll_running and self.is_connected():
                try:
                    result = self.execute_function(
                        function_code=self.poll_request_params.get("function_code", 3),
                        address=self.poll_request_params.get("address", 0),
                        count=self.poll_request_params.get("count", 1),
                        unit_id=self.poll_request_params.get("unit_id", 1),
                    )
                    if callback and self.poll_running:
                        callback(result)
                except Exception as exc:
                    self._log(f"Poll loop error: {exc}", tag="error")
                time.sleep(self.poll_interval)
            self.poll_running = False

        self.poll_thread = threading.Thread(target=_poll_worker, daemon=True)
        self.poll_thread.start()
        self._log(f"Auto-polling started (every {self.poll_interval:.1f}s)", tag="info")
        return True, ""

    def stop_polling(self):
        """Stops ongoing periodic polling."""
        if self.poll_running:
            self.poll_running = False
            self._log("Auto-polling stopped.", tag="info")
