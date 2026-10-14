/*
  ESP32 Modbus TCP WiFi Server Example
  ------------------------------------
  This Arduino sketch configures an ESP32 as a Modbus TCP server (slave)
  connected to your WiFi network. You can test it directly with Communication Studio.

  Required Arduino Library:
  - In Arduino IDE Library Manager: Search for "ModbusIP_ESP8266" by André Sarmento and install it.
    (Note: "ModbusIP_ESP8266" fully supports both ESP8266 and ESP32!)
*/

#include <WiFi.h>
#include <ModbusIP_ESP8266.h>

// --- WiFi Credentials ---
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// ModbusIP instance (Modbus TCP server on default port 502)
ModbusIP mb;

// Modbus Register Offsets
const int LED_COIL_ADDR = 0;         // Coil 0: LED On/Off (FC 01 / FC 05)
const int COUNTER_REG_ADDR = 0;      // Holding Reg 0: Auto-incrementing counter (FC 03)
const int SENSOR_REG_ADDR = 1;       // Holding Reg 1: Simulated sensor value (FC 03)
const int SETPOINT_REG_ADDR = 2;     // Holding Reg 2: Configurable setpoint (FC 03 / FC 06)

const int LED_PIN = 2;               // Onboard LED pin on most ESP32 boards
unsigned long lastUpdate = 0;
uint16_t counterVal = 0;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Connect to WiFi
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.println(">>> Enter this IP address in Communication Studio Modbus TCP Panel! <<<");

  // Start Modbus TCP server (port 502)
  mb.server();

  // Configure Modbus registers & coils
  mb.addCoil(LED_COIL_ADDR, false);        // Coil 0
  mb.addHreg(COUNTER_REG_ADDR, 0);         // Holding Register 0
  mb.addHreg(SENSOR_REG_ADDR, 250);        // Holding Register 1
  mb.addHreg(SETPOINT_REG_ADDR, 100);      // Holding Register 2
}

void loop() {
  // Process incoming Modbus TCP requests
  mb.task();

  // Sync Coil 0 state to onboard LED
  bool ledState = mb.Coil(LED_COIL_ADDR);
  digitalWrite(LED_PIN, ledState ? HIGH : LOW);

  // Periodically update simulated register values every 1 second
  if (millis() - lastUpdate > 1000) {
    lastUpdate = millis();

    counterVal++;
    mb.Hreg(COUNTER_REG_ADDR, counterVal);

    // Simulated sensor reading (e.g. 200 - 300)
    uint16_t simulatedSensor = 240 + (counterVal % 50);
    mb.Hreg(SENSOR_REG_ADDR, simulatedSensor);
  }

  delay(10);
}
