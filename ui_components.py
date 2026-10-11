import tkinter as tk
from datetime import datetime
from tkinter import filedialog, ttk


class AppUI:

  def __init__(
      self,
      root,
      on_connect_toggle,
      on_send,
      on_refresh_ports,
      on_clear_sent,
      on_clear_recv,
      on_save_logs,
  ):
    self.root = root
    self.root.title("Advanced Serial Monitor")
    self.root.geometry("850x500")
    self.root.minsize(700, 450)

    # Configure root grid scaling
    self.root.rowconfigure(1, weight=1)
    self.root.columnconfigure(0, weight=1)

    # --- Top Frame: Port & Baudrate Selection ---
    top_frame = ttk.Frame(root, padding=10)
    top_frame.grid(row=0, column=0, sticky="ew")

    ttk.Label(top_frame, text="Port:").pack(side=tk.LEFT, padx=(0, 5))

    self.port_combobox = ttk.Combobox(top_frame, width=15, state="readonly")
    self.port_combobox.pack(side=tk.LEFT, padx=5)

    self.refresh_btn = ttk.Button(
        top_frame, text="Refresh", command=on_refresh_ports
    )
    self.refresh_btn.pack(side=tk.LEFT, padx=5)

    ttk.Label(top_frame, text="Baud:").pack(side=tk.LEFT, padx=(15, 5))

    self.baud_combobox = ttk.Combobox(top_frame, width=10, state="readonly")
    self.baud_combobox["values"] = [
        "9600",
        "19200",
        "38400",
        "57600",
        "115200",
        "230400",
        "500000",
        "921600",
    ]
    self.baud_combobox.set("115200")
    self.baud_combobox.pack(side=tk.LEFT, padx=5)

    self.connect_btn = ttk.Button(
        top_frame, text="Connect", command=on_connect_toggle
    )
    self.connect_btn.pack(side=tk.LEFT, padx=(15, 5))

    self.status_var = tk.StringVar(value="Disconnected")
    self.status_label = ttk.Label(
        top_frame,
        textvariable=self.status_var,
        font=("Arial", 9, "bold"),
        foreground="#d9534f",
    )
    self.status_label.pack(side=tk.LEFT, padx=(5, 5))

    self.save_btn = ttk.Button(top_frame, text="Save Logs", command=on_save_logs)
    self.save_btn.pack(side=tk.LEFT, padx=(10, 0))

    # --- Main Content Frame (Split Left / Right) ---
    content_frame = ttk.Frame(root, padding=10)
    content_frame.grid(row=1, column=0, sticky="nsew")
    content_frame.rowconfigure(0, weight=1)
    content_frame.columnconfigure(0, weight=1)
    content_frame.columnconfigure(1, weight=1)

    # --- Left Side: Input & Send ---
    left_frame = ttk.LabelFrame(
        content_frame, text=" Control Panel ", padding=10
    )
    left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
    left_frame.rowconfigure(2, weight=1)
    left_frame.columnconfigure(0, weight=1)

    ttk.Label(left_frame, text="Enter Your Message:").grid(
        row=0, column=0, sticky="w", pady=(0, 5)
    )

    self.entry_box = ttk.Entry(left_frame, font=("Arial", 12))
    self.entry_box.grid(row=1, column=0, sticky="ew", pady=(0, 10))

    self.send_btn = ttk.Button(
        left_frame, text="Send", command=on_send, state=tk.DISABLED
    )
    self.send_btn.grid(row=2, column=0, sticky="n", ipadx=10, ipady=5)

    # --- Right Side: Command Terminals (Sent & Received) ---
    right_frame = ttk.Frame(content_frame)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
    right_frame.rowconfigure(0, weight=1)
    right_frame.rowconfigure(1, weight=1)
    right_frame.columnconfigure(0, weight=1)

    # Upper Right: Sent Log Container
    sent_container = ttk.Frame(right_frame)
    sent_container.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
    sent_container.rowconfigure(1, weight=1)
    sent_container.columnconfigure(0, weight=1)

    sent_header = ttk.Frame(sent_container)
    sent_header.grid(row=0, column=0, sticky="ew", pady=(0, 2))
    ttk.Label(sent_header, text="Sent Log", font=("Arial", 9, "bold")).pack(
        side=tk.LEFT
    )
    ttk.Button(
        sent_header, text="Clear", width=6, command=on_clear_sent
    ).pack(side=tk.RIGHT)

    sent_box_frame = ttk.Frame(sent_container)
    sent_box_frame.grid(row=1, column=0, sticky="nsew")
    sent_box_frame.rowconfigure(0, weight=1)
    sent_box_frame.columnconfigure(0, weight=1)
    self.sent_text = self._create_terminal(sent_box_frame)

    # Lower Right: Received Log Container
    recv_container = ttk.Frame(right_frame)
    recv_container.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
    recv_container.rowconfigure(1, weight=1)
    recv_container.columnconfigure(0, weight=1)

    recv_header = ttk.Frame(recv_container)
    recv_header.grid(row=0, column=0, sticky="ew", pady=(0, 2))
    ttk.Label(recv_header, text="Received Log", font=("Arial", 9, "bold")).pack(
        side=tk.LEFT
    )
    ttk.Button(
        recv_header, text="Clear", width=6, command=on_clear_recv
    ).pack(side=tk.RIGHT)

    recv_box_frame = ttk.Frame(recv_container)
    recv_box_frame.grid(row=1, column=0, sticky="nsew")
    recv_box_frame.rowconfigure(0, weight=1)
    recv_box_frame.columnconfigure(0, weight=1)
    self.recv_text = self._create_terminal(recv_box_frame)

  def _create_terminal(self, parent):
    """Helper to create a retro CMD-looking text widget with a scrollbar."""
    text_widget = tk.Text(
        parent,
        bg="#1e1e1e",
        fg="#00ff00",
        insertbackground="white",
        font=("Courier", 10),
        state=tk.DISABLED,
        wrap=tk.WORD,
    )
    scrollbar = ttk.Scrollbar(
        parent, orient="vertical", command=text_widget.yview
    )
    text_widget.configure(yscrollcommand=scrollbar.set)

    text_widget.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    return text_widget

  def set_status(self, message, connected):
    """Updates the connection status indicator."""
    self.status_var.set(message)
    self.status_label.config(foreground="#2ca02c" if connected else "#d9534f")

  @staticmethod
  def _timestamp():
    return datetime.now().strftime("%H:%M:%S")

  def append_log(self, text_widget, message):
    """Appends text thread-safely to a terminal widget and auto-scrolls."""
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, f"[{self._timestamp()}] {message}\n")
    text_widget.see(tk.END)
    text_widget.config(state=tk.DISABLED)

  def clear_log(self, text_widget):
    """Clears all text from a terminal widget."""
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    text_widget.config(state=tk.DISABLED)

  def get_log_text(self, text_widget):
    """Returns the full contents of a terminal widget."""
    return text_widget.get("1.0", tk.END).rstrip()