import tkinter as tk
from datetime import datetime
<<<<<<< HEAD
from tkinter import ttk


class StyleManager:
    """Configures modern colors and ttk widget styles for the entire app."""

    DARK_BG = "#181926"        # Deep charcoal
    CARD_BG = "#24273a"        # Card background
    CARD_HOVER = "#2f334d"     # Card hover background
    BORDER_COLOR = "#363a4f"   # Border lines
    TEXT_MAIN = "#cad3f5"      # Main text
    TEXT_MUTED = "#8087a2"     # Secondary text
    ACCENT_BLUE = "#3a86ff"    # Primary accent blue
    ACCENT_GREEN = "#10b981"   # Success green
    ACCENT_RED = "#ef4444"     # Danger/Disconnected red
    ACCENT_PURPLE = "#8b5cf6"  # Modbus accent
    TERMINAL_BG = "#11121d"    # Terminal screen background
    TERMINAL_FG = "#00ff88"    # Matrix green

    @classmethod
    def apply(cls, root):
        root.configure(bg=cls.DARK_BG)
        style = ttk.Style(root)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Global Frame backgrounds
        style.configure("TFrame", background=cls.DARK_BG)
        style.configure("Card.TFrame", background=cls.CARD_BG, relief="solid", borderwidth=1)
        style.configure("CardInner.TFrame", background=cls.CARD_BG)
        style.configure("CardHover.TFrame", background=cls.CARD_HOVER, relief="solid", borderwidth=1)

        # Label styles
        style.configure("TLabel", background=cls.DARK_BG, foreground=cls.TEXT_MAIN, font=("Arial", 10))
        style.configure("Card.TLabel", background=cls.CARD_BG, foreground=cls.TEXT_MAIN, font=("Arial", 10))
        style.configure("CardMuted.TLabel", background=cls.CARD_BG, foreground=cls.TEXT_MUTED, font=("Arial", 9))
        style.configure("HeroTitle.TLabel", background=cls.DARK_BG, foreground="#ffffff", font=("Arial", 18, "bold"))
        style.configure("HeroSub.TLabel", background=cls.DARK_BG, foreground=cls.TEXT_MUTED, font=("Arial", 10))
        style.configure("CardTitle.TLabel", background=cls.CARD_BG, foreground="#ffffff", font=("Arial", 14, "bold"))
        style.configure("BadgeUart.TLabel", background="#1d3557", foreground="#48cae4", font=("Arial", 8, "bold"), padding=4)
        style.configure("BadgeModbus.TLabel", background="#3b1d57", foreground="#c77dff", font=("Arial", 8, "bold"), padding=4)

        # LabelFrame
        style.configure("TLabelframe", background=cls.CARD_BG, foreground=cls.TEXT_MAIN, bordercolor=cls.BORDER_COLOR)
        style.configure("TLabelframe.Label", background=cls.CARD_BG, foreground="#ffffff", font=("Arial", 10, "bold"))

        # Buttons
        style.configure("TButton", font=("Arial", 9), padding=(8, 4))
        style.configure("Primary.TButton", background=cls.ACCENT_BLUE, foreground="#ffffff", font=("Arial", 9, "bold"))
        style.map("Primary.TButton", background=[("active", "#2563eb"), ("disabled", "#334155")])

        style.configure("Success.TButton", background=cls.ACCENT_GREEN, foreground="#ffffff", font=("Arial", 9, "bold"))
        style.map("Success.TButton", background=[("active", "#059669"), ("disabled", "#334155")])

        style.configure("Danger.TButton", background=cls.ACCENT_RED, foreground="#ffffff", font=("Arial", 9, "bold"))
        style.map("Danger.TButton", background=[("active", "#dc2626"), ("disabled", "#334155")])

        style.configure("Nav.TButton", background=cls.CARD_BG, foreground=cls.TEXT_MAIN, font=("Arial", 9, "bold"))
        style.map("Nav.TButton", background=[("active", cls.CARD_HOVER)])

        # Combobox
        style.configure("TCombobox", fieldbackground="#1e2030", background=cls.CARD_BG, foreground="#ffffff", selectbackground=cls.ACCENT_BLUE)

        # Entry
        style.configure("TEntry", fieldbackground="#1e2030", foreground="#ffffff")

        # Tabs / Notebook
        style.configure("TNotebook", background=cls.DARK_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=cls.CARD_BG, foreground=cls.TEXT_MAIN, padding=(14, 6), font=("Arial", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", cls.ACCENT_BLUE)], foreground=[("selected", "#ffffff")])

        # Treeview (Data grid)
        style.configure("Treeview", background="#1a1c2a", fieldbackground="#1a1c2a", foreground=cls.TEXT_MAIN, rowheight=24, font=("Arial", 9))
        style.configure("Treeview.Heading", background=cls.CARD_BG, foreground="#ffffff", font=("Arial", 9, "bold"), padding=4)
        style.map("Treeview", background=[("selected", cls.ACCENT_BLUE)], foreground=[("selected", "#ffffff")])


def create_terminal(parent, fg_color="#00ff88"):
    """Creates a retro/dark terminal with scrollbar and syntax tags."""
    container = ttk.Frame(parent)
    container.rowconfigure(0, weight=1)
    container.columnconfigure(0, weight=1)

    text_widget = tk.Text(
        container,
        bg=StyleManager.TERMINAL_BG,
        fg=fg_color,
        insertbackground="#ffffff",
        font=("Courier", 10),
        state=tk.DISABLED,
        wrap=tk.WORD,
        relief="flat",
        padx=8,
        pady=8,
    )
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=text_widget.yview)
=======
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
>>>>>>> 5154e379dacb7e6037c2f38987144453a81a3724
    text_widget.configure(yscrollcommand=scrollbar.set)

    text_widget.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
<<<<<<< HEAD

    # Syntax tags
    text_widget.tag_configure("tx", foreground="#f59e0b")        # Amber
    text_widget.tag_configure("rx", foreground="#00ff88")        # Phosphor green
    text_widget.tag_configure("success", foreground="#10b981")   # Emerald
    text_widget.tag_configure("error", foreground="#ef4444")     # Red
    text_widget.tag_configure("info", foreground="#38bdf8")      # Cyan
    text_widget.tag_configure("system", foreground="#94a3b8")    # Gray

    return container, text_widget


class ModeSelectUI:
    """Initial launcher screen to choose between UART and MODBUS."""

    def __init__(self, parent, on_select_uart, on_select_modbus):
        self.frame = ttk.Frame(parent, style="TFrame")
        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(0, weight=1)

        # Header Hero
        header_frame = ttk.Frame(self.frame, style="TFrame", padding=(20, 25, 20, 15))
        header_frame.grid(row=0, column=0, sticky="ew")

        ttk.Label(
            header_frame,
            text="COMMUNICATION STUDIO",
            style="HeroTitle.TLabel",
        ).pack(anchor="center")

        ttk.Label(
            header_frame,
            text="Universal Diagnostic & Monitoring Suite for Microcontrollers & Industrial Protocols",
            style="HeroSub.TLabel",
        ).pack(anchor="center", pady=(4, 0))

        # Subtitle instructions
        prompt_frame = ttk.Frame(self.frame, style="TFrame", padding=(20, 5))
        prompt_frame.grid(row=1, column=0, sticky="ew")
        ttk.Label(
            prompt_frame,
            text="Please select the protocol you want to work with:",
            font=("Arial", 11, "bold"),
            foreground="#cad3f5",
        ).pack(anchor="center")

        # Cards Container
        cards_container = ttk.Frame(self.frame, style="TFrame", padding=(30, 20))
        cards_container.grid(row=2, column=0, sticky="nsew")
        cards_container.rowconfigure(0, weight=1)
        cards_container.columnconfigure(0, weight=1, uniform="card")
        cards_container.columnconfigure(1, weight=1, uniform="card")

        # --- Card 1: UART ---
        self.uart_card = ttk.Frame(cards_container, style="Card.TFrame", padding=20)
        self.uart_card.grid(row=0, column=0, sticky="nsew", padx=15, pady=10)
        self.uart_card.rowconfigure(4, weight=1)

        ttk.Label(self.uart_card, text=" USB / SERIAL COM ", style="BadgeUart.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(self.uart_card, text="UART Serial Monitor", style="CardTitle.TLabel").grid(row=1, column=0, sticky="w", pady=(10, 4))
        ttk.Label(
            self.uart_card,
            text="Direct bidirectional serial communication over USB cable. Ideal for Arduino, ESP32 USB debug, and STM32.",
            style="CardMuted.TLabel",
            wraplength=340,
            justify="left",
        ).grid(row=2, column=0, sticky="w", pady=(0, 15))

        uart_bullets = [
            "✔  Auto-scan USB COM ports & baud rates",
            "✔  Real-time separate Sent & Received terminals",
            "✔  Custom baud rates (up to 921600)",
            "✔  Save debug communication logs to .txt",
        ]
        bullet_frame1 = ttk.Frame(self.uart_card, style="CardInner.TFrame")
        bullet_frame1.grid(row=3, column=0, sticky="w", pady=(0, 20))
        for b in uart_bullets:
            ttk.Label(bullet_frame1, text=b, style="Card.TLabel").pack(anchor="w", pady=2)

        uart_btn = ttk.Button(
            self.uart_card,
            text="Launch UART Monitor  ➜",
            style="Primary.TButton",
            command=on_select_uart,
        )
        uart_btn.grid(row=5, column=0, sticky="ew", ipady=6)

        # --- Card 2: MODBUS ---
        self.modbus_card = ttk.Frame(cards_container, style="Card.TFrame", padding=20)
        self.modbus_card.grid(row=0, column=1, sticky="nsew", padx=15, pady=10)
        self.modbus_card.rowconfigure(4, weight=1)

        ttk.Label(self.modbus_card, text=" TCP (WIFI/LAN) & RTU ", style="BadgeModbus.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(self.modbus_card, text="MODBUS Diagnostic Studio", style="CardTitle.TLabel").grid(row=1, column=0, sticky="w", pady=(10, 4))
        ttk.Label(
            self.modbus_card,
            text="Industrial standard protocol tester. Connect to ESP32 over WiFi via Modbus TCP to read/write registers & coils.",
            style="CardMuted.TLabel",
            wraplength=340,
            justify="left",
        ).grid(row=2, column=0, sticky="w", pady=(0, 15))

        modbus_bullets = [
            "✔  Modbus TCP Client over WiFi / Ethernet",
            "✔  Read & Write Coils and Holding/Input Registers",
            "✔  Live Data Table (Decimal, Hex & Binary)",
            "✔  Automated Periodic Polling & Transaction Log",
        ]
        bullet_frame2 = ttk.Frame(self.modbus_card, style="CardInner.TFrame")
        bullet_frame2.grid(row=3, column=0, sticky="w", pady=(0, 20))
        for b in modbus_bullets:
            ttk.Label(bullet_frame2, text=b, style="Card.TLabel").pack(anchor="w", pady=2)

        modbus_btn = ttk.Button(
            self.modbus_card,
            text="Launch MODBUS Studio  ➜",
            style="Primary.TButton",
            command=on_select_modbus,
        )
        modbus_btn.grid(row=5, column=0, sticky="ew", ipady=6)

        # Footer
        footer_frame = ttk.Frame(self.frame, style="TFrame", padding=(20, 10))
        footer_frame.grid(row=3, column=0, sticky="ew")
        ttk.Label(
            footer_frame,
            text="Tip: You can seamlessly switch between UART and MODBUS anytime from the top navigation bar.",
            style="HeroSub.TLabel",
        ).pack(anchor="center")


class UartUI:
    """Modern UI layout for UART Serial Monitor."""

    def __init__(
        self,
        parent,
        on_back,
        on_connect_toggle,
        on_send,
        on_refresh_ports,
        on_clear_sent,
        on_clear_recv,
        on_save_logs,
    ):
        self.frame = ttk.Frame(parent, style="TFrame")
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)

        # --- Top Navigation & Control Bar ---
        nav_frame = ttk.Frame(self.frame, style="Card.TFrame", padding=(10, 8))
        nav_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        # Back Button
        ttk.Button(
            nav_frame,
            text="⬅ Back to Modes",
            style="Nav.TButton",
            command=on_back,
        ).pack(side=tk.LEFT, padx=(0, 15))

        # Title & Mode
        ttk.Label(
            nav_frame,
            text="UART Monitor",
            font=("Arial", 11, "bold"),
            style="Card.TLabel",
        ).pack(side=tk.LEFT, padx=(0, 15))

        # Port selection
        ttk.Label(nav_frame, text="Port:", style="Card.TLabel").pack(side=tk.LEFT, padx=(0, 4))
        self.port_combobox = ttk.Combobox(nav_frame, width=14, state="readonly")
        self.port_combobox.pack(side=tk.LEFT, padx=(0, 5))

        self.refresh_btn = ttk.Button(nav_frame, text="↻ Refresh", command=on_refresh_ports)
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 12))

        # Baud rate selection
        ttk.Label(nav_frame, text="Baud:", style="Card.TLabel").pack(side=tk.LEFT, padx=(0, 4))
        self.baud_combobox = ttk.Combobox(nav_frame, width=9, state="readonly")
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
        self.baud_combobox.pack(side=tk.LEFT, padx=(0, 12))

        # Connect Button
        self.connect_btn = ttk.Button(
            nav_frame,
            text="Connect",
            style="Success.TButton",
            command=on_connect_toggle,
        )
        self.connect_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Status Label
        self.status_var = tk.StringVar(value="● Disconnected")
        self.status_label = ttk.Label(
            nav_frame,
            textvariable=self.status_var,
            font=("Arial", 9, "bold"),
            foreground=StyleManager.ACCENT_RED,
            style="Card.TLabel",
        )
        self.status_label.pack(side=tk.LEFT, padx=(0, 15))

        # Save Logs Button
        self.save_btn = ttk.Button(nav_frame, text="💾 Save Logs", command=on_save_logs)
        self.save_btn.pack(side=tk.RIGHT)

        # --- Main Content Frame (Split Left / Right) ---
        content_frame = ttk.Frame(self.frame, style="TFrame", padding=10)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.rowconfigure(0, weight=1)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=2)

        # --- Left Side: Control Panel ---
        left_frame = ttk.LabelFrame(content_frame, text=" Serial Transmitter ", padding=12)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        left_frame.columnconfigure(0, weight=1)

        ttk.Label(
            left_frame,
            text="Enter Message to Send:",
            font=("Arial", 10, "bold"),
            style="Card.TLabel",
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.entry_box = ttk.Entry(left_frame, font=("Arial", 11))
        self.entry_box.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        self.send_btn = ttk.Button(
            left_frame,
            text="Send  ➜",
            style="Primary.TButton",
            command=on_send,
            state=tk.DISABLED,
        )
        self.send_btn.grid(row=2, column=0, sticky="ew", ipady=4, pady=(0, 15))

        # Helpful hints
        hint_box = ttk.Frame(left_frame, style="CardInner.TFrame")
        hint_box.grid(row=3, column=0, sticky="nsew", pady=10)
        ttk.Label(
            hint_box,
            text="Keyboard Shortcut:\n• Press Enter in input field to send\n\nProtocol Format:\n• Messages sent as UTF-8 + newline (\\n)\n• Suitable for ESP32/Arduino Serial.readStringUntil('\\n')",
            style="CardMuted.TLabel",
            justify="left",
        ).pack(anchor="w")

        # --- Right Side: Command Terminals (Sent & Received) ---
        right_frame = ttk.Frame(content_frame, style="TFrame")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        right_frame.rowconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)

        # Upper Right: Sent Log
        sent_container = ttk.Frame(right_frame, style="Card.TFrame", padding=6)
        sent_container.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        sent_container.rowconfigure(1, weight=1)
        sent_container.columnconfigure(0, weight=1)

        sent_header = ttk.Frame(sent_container, style="CardInner.TFrame")
        sent_header.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        ttk.Label(sent_header, text="📤 Sent Messages Log", font=("Arial", 9, "bold"), style="Card.TLabel").pack(side=tk.LEFT)
        ttk.Button(sent_header, text="Clear", width=6, command=on_clear_sent).pack(side=tk.RIGHT)

        sent_term_container, self.sent_text = create_terminal(sent_container, fg_color="#fbbf24")
        sent_term_container.grid(row=1, column=0, sticky="nsew")

        # Lower Right: Received Log
        recv_container = ttk.Frame(right_frame, style="Card.TFrame", padding=6)
        recv_container.grid(row=1, column=0, sticky="nsew", pady=(4, 0))
        recv_container.rowconfigure(1, weight=1)
        recv_container.columnconfigure(0, weight=1)

        recv_header = ttk.Frame(recv_container, style="CardInner.TFrame")
        recv_header.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        ttk.Label(recv_header, text="📥 Received Messages Log", font=("Arial", 9, "bold"), style="Card.TLabel").pack(side=tk.LEFT)
        ttk.Button(recv_header, text="Clear", width=6, command=on_clear_recv).pack(side=tk.RIGHT)

        recv_term_container, self.recv_text = create_terminal(recv_container, fg_color="#00ff88")
        recv_term_container.grid(row=1, column=0, sticky="nsew")

    def set_status(self, text, connected):
        """Updates connection state and badge color."""
        self.status_var.set(f"● {text}")
        color = StyleManager.ACCENT_GREEN if connected else StyleManager.ACCENT_RED
        self.status_label.config(foreground=color)

    @staticmethod
    def _timestamp():
        return datetime.now().strftime("%H:%M:%S")

    def append_log(self, text_widget, message, tag=None):
        """Appends timestamped text to terminal widget."""
        text_widget.config(state=tk.NORMAL)
        msg_formatted = f"[{self._timestamp()}] {message}\n"
        if tag:
            text_widget.insert(tk.END, msg_formatted, tag)
        else:
            text_widget.insert(tk.END, msg_formatted)
        text_widget.see(tk.END)
        text_widget.config(state=tk.DISABLED)

    def clear_log(self, text_widget):
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        text_widget.config(state=tk.DISABLED)

    def get_log_text(self, text_widget):
        return text_widget.get("1.0", tk.END).rstrip()


class ModbusUI:
    """Modern UI layout for Modbus Diagnostic Studio (Modbus TCP & RTU option)."""

    def __init__(
        self,
        parent,
        on_back,
        on_connect_toggle,
        on_execute,
        on_toggle_poll,
        on_clear_table,
        on_clear_log,
        on_save_logs,
    ):
        self.frame = ttk.Frame(parent, style="TFrame")
        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.on_execute = on_execute
        self.on_toggle_poll = on_toggle_poll

        # --- Top Navigation Bar ---
        nav_frame = ttk.Frame(self.frame, style="Card.TFrame", padding=(10, 8))
        nav_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 4))

        ttk.Button(
            nav_frame,
            text="⬅ Back to Modes",
            style="Nav.TButton",
            command=on_back,
        ).pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(
            nav_frame,
            text="MODBUS Studio",
            font=("Arial", 11, "bold"),
            style="Card.TLabel",
        ).pack(side=tk.LEFT, padx=(0, 20))

        # Protocol Type Selector (TCP vs RTU)
        ttk.Label(nav_frame, text="Protocol Mode:", style="Card.TLabel").pack(side=tk.LEFT, padx=(0, 5))
        self.protocol_mode = tk.StringVar(value="tcp")

        self.radio_tcp = ttk.Radiobutton(
            nav_frame,
            text="MODBUS TCP (WiFi/LAN)",
            variable=self.protocol_mode,
            value="tcp",
            command=self._on_protocol_change,
        )
        self.radio_tcp.pack(side=tk.LEFT, padx=(0, 10))

        self.radio_rtu = ttk.Radiobutton(
            nav_frame,
            text="MODBUS RTU (Serial - Coming Soon)",
            variable=self.protocol_mode,
            value="rtu",
            command=self._on_protocol_change,
        )
        self.radio_rtu.pack(side=tk.LEFT, padx=(0, 15))

        # Save Logs button on right
        ttk.Button(nav_frame, text="💾 Save Logs", command=on_save_logs).pack(side=tk.RIGHT)

        # --- Container for Views (TCP view vs RTU placeholder) ---
        self.subviews_container = ttk.Frame(self.frame, style="TFrame")
        self.subviews_container.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=10, pady=5)
        self.subviews_container.rowconfigure(0, weight=1)
        self.subviews_container.columnconfigure(0, weight=1)

        # Build Subviews
        self._build_tcp_view(on_connect_toggle, on_execute, on_clear_table, on_clear_log)
        self._build_rtu_placeholder()

        # Show initial view (TCP)
        self.tcp_frame.grid(row=0, column=0, sticky="nsew")

    def _on_protocol_change(self):
        """Switches between TCP view and RTU placeholder view."""
        mode = self.protocol_mode.get()
        if mode == "tcp":
            self.rtu_frame.grid_forget()
            self.tcp_frame.grid(row=0, column=0, sticky="nsew")
        else:
            self.tcp_frame.grid_forget()
            self.rtu_frame.grid(row=0, column=0, sticky="nsew")

    def _build_tcp_view(self, on_connect_toggle, on_execute, on_clear_table, on_clear_log):
        """Constructs the full Modbus TCP control and monitoring panel."""
        self.tcp_frame = ttk.Frame(self.subviews_container, style="TFrame")
        self.tcp_frame.rowconfigure(2, weight=1)
        self.tcp_frame.columnconfigure(0, weight=1)

        # --- Row 0: TCP Connection Settings Card ---
        conn_card = ttk.LabelFrame(self.tcp_frame, text=" Modbus TCP Connection ", padding=(10, 8))
        conn_card.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        # Target IP / Host
        ttk.Label(conn_card, text="Slave IP:", style="Card.TLabel").pack(side=tk.LEFT, padx=(0, 4))
        self.ip_entry = ttk.Entry(conn_card, width=15)
        self.ip_entry.insert(0, "192.168.1.100")
        self.ip_entry.pack(side=tk.LEFT, padx=(0, 10))

        # Port
        ttk.Label(conn_card, text="Port:", style="Card.TLabel").pack(side=tk.LEFT, padx=(0, 4))
        self.port_entry = ttk.Entry(conn_card, width=6)
        self.port_entry.insert(0, "502")
        self.port_entry.pack(side=tk.LEFT, padx=(0, 10))

        # Unit / Device ID
        ttk.Label(conn_card, text="Unit ID:", style="Card.TLabel").pack(side=tk.LEFT, padx=(0, 4))
        self.unit_entry = ttk.Entry(conn_card, width=5)
        self.unit_entry.insert(0, "1")
        self.unit_entry.pack(side=tk.LEFT, padx=(0, 10))

        # Timeout
        ttk.Label(conn_card, text="Timeout(s):", style="Card.TLabel").pack(side=tk.LEFT, padx=(0, 4))
        self.timeout_entry = ttk.Entry(conn_card, width=5)
        self.timeout_entry.insert(0, "3.0")
        self.timeout_entry.pack(side=tk.LEFT, padx=(0, 15))

        # Connect Button
        self.connect_btn = ttk.Button(
            conn_card,
            text="Connect",
            style="Success.TButton",
            command=on_connect_toggle,
        )
        self.connect_btn.pack(side=tk.LEFT, padx=(0, 12))

        # Status Badge
        self.status_var = tk.StringVar(value="● Disconnected")
        self.status_label = ttk.Label(
            conn_card,
            textvariable=self.status_var,
            font=("Arial", 9, "bold"),
            foreground=StyleManager.ACCENT_RED,
            style="Card.TLabel",
        )
        self.status_label.pack(side=tk.LEFT, padx=(0, 10))

        # --- Row 1: Operations Panel ---
        ops_card = ttk.LabelFrame(self.tcp_frame, text=" Modbus Operations & Requests ", padding=(10, 8))
        ops_card.grid(row=1, column=0, sticky="ew", pady=(0, 6))

        # Function Code
        ttk.Label(ops_card, text="Function:", style="Card.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 4), pady=2)
        self.func_combobox = ttk.Combobox(ops_card, width=28, state="readonly")
        self.func_combobox["values"] = [
            "01: Read Coils (FC 01)",
            "02: Read Discrete Inputs (FC 02)",
            "03: Read Holding Registers (FC 03)",
            "04: Read Input Registers (FC 04)",
            "05: Write Single Coil (FC 05)",
            "06: Write Single Register (FC 06)",
            "15: Write Multiple Coils (FC 15)",
            "16: Write Multiple Registers (FC 16)",
        ]
        self.func_combobox.set("03: Read Holding Registers (FC 03)")
        self.func_combobox.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=2)
        self.func_combobox.bind("<<ComboboxSelected>>", self._on_func_selected)

        # Address
        ttk.Label(ops_card, text="Address:", style="Card.TLabel").grid(row=0, column=2, sticky="w", padx=(0, 4), pady=2)
        self.addr_entry = ttk.Entry(ops_card, width=7)
        self.addr_entry.insert(0, "0")
        self.addr_entry.grid(row=0, column=3, sticky="w", padx=(0, 10), pady=2)

        # Count
        ttk.Label(ops_card, text="Count:", style="Card.TLabel").grid(row=0, column=4, sticky="w", padx=(0, 4), pady=2)
        self.count_entry = ttk.Entry(ops_card, width=6)
        self.count_entry.insert(0, "1")
        self.count_entry.grid(row=0, column=5, sticky="w", padx=(0, 10), pady=2)

        # Value(s) to Write
        ttk.Label(ops_card, text="Value(s):", style="Card.TLabel").grid(row=0, column=6, sticky="w", padx=(0, 4), pady=2)
        self.value_entry = ttk.Entry(ops_card, width=16)
        self.value_entry.insert(0, "0")
        self.value_entry.grid(row=0, column=7, sticky="w", padx=(0, 10), pady=2)

        # Execute Button
        self.exec_btn = ttk.Button(
            ops_card,
            text="Execute Request",
            style="Primary.TButton",
            command=on_execute,
            state=tk.DISABLED,
        )
        self.exec_btn.grid(row=0, column=8, sticky="w", padx=(10, 10), pady=2)

        # Polling Controls Frame
        poll_subframe = ttk.Frame(ops_card, style="CardInner.TFrame")
        poll_subframe.grid(row=1, column=0, columnspan=9, sticky="ew", pady=(6, 0))

        # Dynamic instruction helper label
        self.hint_label = ttk.Label(
            poll_subframe,
            text="Read Holding Registers: Reads 'Count' registers starting at 'Address'. Value is ignored for reads.",
            style="CardMuted.TLabel",
        )
        self.hint_label.pack(side=tk.LEFT)

        # Auto-poll controls
        self.poll_var = tk.BooleanVar(value=False)
        self.poll_check = ttk.Checkbutton(
            poll_subframe,
            text="Auto-Poll Every:",
            variable=self.poll_var,
            command=self.on_toggle_poll,
            state=tk.DISABLED,
        )
        self.poll_check.pack(side=tk.RIGHT, padx=(5, 0))

        self.poll_interval_combo = ttk.Combobox(poll_subframe, width=8, state="readonly")
        self.poll_interval_combo["values"] = ["500 ms", "1000 ms", "2000 ms", "5000 ms"]
        self.poll_interval_combo.set("1000 ms")
        self.poll_interval_combo.pack(side=tk.RIGHT)

        # --- Row 2: Tabs (Data Table & Transaction Log) ---
        notebook_frame = ttk.Frame(self.tcp_frame, style="TFrame")
        notebook_frame.grid(row=2, column=0, sticky="nsew", pady=(4, 0))
        notebook_frame.rowconfigure(0, weight=1)
        notebook_frame.columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # Tab 1: Live Register View Table
        tab_table = ttk.Frame(self.notebook, style="Card.TFrame", padding=6)
        tab_table.rowconfigure(1, weight=1)
        tab_table.columnconfigure(0, weight=1)
        self.notebook.add(tab_table, text="  📊 Live Register View  ")

        table_header = ttk.Frame(tab_table, style="CardInner.TFrame")
        table_header.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        ttk.Label(table_header, text="Microcontroller Registers & Coils Table", font=("Arial", 9, "bold"), style="Card.TLabel").pack(side=tk.LEFT)
        ttk.Button(table_header, text="Clear Table", width=12, command=on_clear_table).pack(side=tk.RIGHT)

        columns = ("addr", "type", "dec", "hex", "bin", "time")
        self.tree = ttk.Treeview(tab_table, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("addr", text="Address (Hex / Dec)")
        self.tree.heading("type", text="Register Type")
        self.tree.heading("dec", text="Decimal Value")
        self.tree.heading("hex", text="Hexadecimal")
        self.tree.heading("bin", text="Binary / State")
        self.tree.heading("time", text="Last Updated")

        self.tree.column("addr", width=140, anchor="center")
        self.tree.column("type", width=130, anchor="center")
        self.tree.column("dec", width=100, anchor="center")
        self.tree.column("hex", width=110, anchor="center")
        self.tree.column("bin", width=140, anchor="center")
        self.tree.column("time", width=110, anchor="center")

        tree_scroll = ttk.Scrollbar(tab_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.grid(row=1, column=0, sticky="nsew")
        tree_scroll.grid(row=1, column=1, sticky="ns")

        # Tab 2: Transaction Log Terminal
        tab_log = ttk.Frame(self.notebook, style="Card.TFrame", padding=6)
        tab_log.rowconfigure(1, weight=1)
        tab_log.columnconfigure(0, weight=1)
        self.notebook.add(tab_log, text="  📜 Communication Terminal  ")

        log_header = ttk.Frame(tab_log, style="CardInner.TFrame")
        log_header.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        ttk.Label(log_header, text="Modbus TCP Transactions & Frame Log", font=("Arial", 9, "bold"), style="Card.TLabel").pack(side=tk.LEFT)
        ttk.Button(log_header, text="Clear Log", width=10, command=on_clear_log).pack(side=tk.RIGHT)

        log_term_container, self.log_text = create_terminal(tab_log, fg_color="#38bdf8")
        log_term_container.grid(row=1, column=0, sticky="nsew")

    def _build_rtu_placeholder(self):
        """Constructs placeholder screen for Modbus RTU."""
        self.rtu_frame = ttk.Frame(self.subviews_container, style="Card.TFrame", padding=30)
        self.rtu_frame.rowconfigure(0, weight=1)
        self.rtu_frame.columnconfigure(0, weight=1)

        center_box = ttk.Frame(self.rtu_frame, style="CardInner.TFrame")
        center_box.grid(row=0, column=0)

        ttk.Label(
            center_box,
            text="MODBUS RTU (Serial RS-485)",
            font=("Arial", 16, "bold"),
            foreground="#ffffff",
            style="Card.TLabel",
        ).pack(anchor="center", pady=(0, 10))

        ttk.Label(
            center_box,
            text="Modbus RTU serial mode is scheduled for an upcoming release.\nFor communicating with your ESP32 or microcontroller over WiFi, please switch to MODBUS TCP mode.",
            style="CardMuted.TLabel",
            justify="center",
        ).pack(anchor="center", pady=(0, 20))

        ttk.Button(
            center_box,
            text="Switch to MODBUS TCP (WiFi)",
            style="Primary.TButton",
            command=lambda: (self.protocol_mode.set("tcp"), self._on_protocol_change()),
        ).pack(anchor="center", ipady=4)

    def _on_func_selected(self, _event=None):
        """Updates hint label and input states based on selected Modbus function."""
        func_str = self.func_combobox.get()
        if "01:" in func_str:
            self.hint_label.config(text="FC01 Read Coils: Reads binary coils (0 or 1). Specify Start Address and Count.")
            self.count_entry.config(state=tk.NORMAL)
            self.value_entry.config(state=tk.DISABLED)
        elif "02:" in func_str:
            self.hint_label.config(text="FC02 Read Discrete Inputs: Reads read-only inputs (0 or 1). Specify Start Address and Count.")
            self.count_entry.config(state=tk.NORMAL)
            self.value_entry.config(state=tk.DISABLED)
        elif "03:" in func_str:
            self.hint_label.config(text="FC03 Read Holding Registers: Reads 16-bit registers. Specify Start Address and Count.")
            self.count_entry.config(state=tk.NORMAL)
            self.value_entry.config(state=tk.DISABLED)
        elif "04:" in func_str:
            self.hint_label.config(text="FC04 Read Input Registers: Reads read-only 16-bit registers. Specify Start Address and Count.")
            self.count_entry.config(state=tk.NORMAL)
            self.value_entry.config(state=tk.DISABLED)
        elif "05:" in func_str:
            self.hint_label.config(text="FC05 Write Single Coil: Enter '1' for ON or '0' for OFF in Value field.")
            self.count_entry.config(state=tk.DISABLED)
            self.value_entry.config(state=tk.NORMAL)
        elif "06:" in func_str:
            self.hint_label.config(text="FC06 Write Single Register: Enter 16-bit integer (0 to 65535) in Value field.")
            self.count_entry.config(state=tk.DISABLED)
            self.value_entry.config(state=tk.NORMAL)
        elif "15:" in func_str:
            self.hint_label.config(text="FC15 Write Multiple Coils: Enter comma-separated values, e.g. 1, 0, 1")
            self.count_entry.config(state=tk.DISABLED)
            self.value_entry.config(state=tk.NORMAL)
        elif "16:" in func_str:
            self.hint_label.config(text="FC16 Write Multiple Registers: Enter comma-separated integers, e.g. 100, 200, 300")
            self.count_entry.config(state=tk.DISABLED)
            self.value_entry.config(state=tk.NORMAL)

    def set_status(self, text, connected):
        """Updates connection state and badge color."""
        self.status_var.set(f"● {text}")
        color = StyleManager.ACCENT_GREEN if connected else StyleManager.ACCENT_RED
        self.status_label.config(foreground=color)

    def update_table_data(self, reg_type, start_addr, values):
        """Updates or inserts register values in the data grid table."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        for i, val in enumerate(values):
            curr_addr = start_addr + i
            hex_addr = f"0x{curr_addr:04X} ({curr_addr})"
            dec_val = str(val)

            if "Coil" in reg_type or "Discrete" in reg_type:
                hex_val = f"0x{val:02X}"
                bin_val = "ON (1)" if val else "OFF (0)"
            else:
                hex_val = f"0x{val:04X}"
                bin_val = f"{val:016b}"

            # Check if address already in treeview
            item_id = f"{reg_type}_{curr_addr}"
            if self.tree.exists(item_id):
                self.tree.item(item_id, values=(hex_addr, reg_type, dec_val, hex_val, bin_val, timestamp))
            else:
                self.tree.insert("", "end", iid=item_id, values=(hex_addr, reg_type, dec_val, hex_val, bin_val, timestamp))

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def append_log(self, message, tag=None):
        self.log_text.config(state=tk.NORMAL)
        if tag:
            self.log_text.insert(tk.END, f"{message}\n", tag)
        else:
            self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def clear_log(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)

    def get_log_text(self):
        return self.log_text.get("1.0", tk.END).rstrip()
=======
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
>>>>>>> 5154e379dacb7e6037c2f38987144453a81a3724
