# Security Alarm System with Alerts Using Arduino 🚨

![Arduino](https://img.shields.io/badge/Hardware-Arduino_Uno-blue)
![Python](https://img.shields.io/badge/Software-Python_3.x-yellow)
![IoT](https://img.shields.io/badge/Tech-IoT_Security-green)

## 📖 Abstract
This project is a cost-effective, real-time security alarm system designed to detect unauthorized intrusions and monitor environmental conditions. It integrates an **Arduino Uno** with ultrasonic, PIR, and temperature sensors to detect motion, proximity breaches, and temperature anomalies.

Upon detecting a threat, the system triggers a local **buzzer** and simultaneously sends **instant alerts to a Telegram Bot** via a Python script. This dual-alert mechanism ensures users are notified immediately, regardless of their location, bridging the gap between embedded systems and modern IoT communication.

## ✨ Key Features
* **Motion Detection:** Uses a PIR sensor to detect human movement within a specific range.
* **Proximity Alert:** Uses an Ultrasonic sensor (HC-SR04) to detect objects within a critical distance (e.g., <10 cm).
* **Environmental Monitoring:** Integrated DHT11 sensor monitors ambient temperature and humidity to detect anomalies (e.g., fire hazards).
* **Real-Time Remote Alerts:** Sends instant notifications to the user's smartphone via the **Telegram App** using a Python-based serial interface.
* **Local Alarm:** Activates an active buzzer immediately upon detection for on-site deterrence.

## 🛠️ Hardware Requirements
* **Microcontroller:** Arduino Uno (ATmega328P)
* **Sensors:**
    * PIR Motion Sensor (HC-SR501)
    * Ultrasonic Sensor (HC-SR04)
    * DHT11 Temperature & Humidity Sensor
* **Output:** Active Buzzer
* **Connectivity:** USB Cable (Type A to B) for Serial Communication
* **Components:** Breadboard, Jumper Wires (M-M, M-F)

## 🔌 Pin Connections
| Component | Pin Name | Arduino Pin | Description |
| :--- | :--- | :--- | :--- |
| **Ultrasonic (HC-SR04)** | TRIG | D9 | Triggers ultrasonic pulse |
| | ECHO | D10 | Receives reflected pulse |
| | VCC/GND | 5V/GND | Power |
| **PIR Sensor** | OUT | D2 | Sends HIGH signal on motion |
| **DHT11 Sensor** | DATA | D7 | Sends temp/humidity data |
| **Buzzer** | POS (+) | D8 | Active High to trigger sound |

> **Note:** Pin assignments in the code must match this table.

## 💻 Software Stack
1.  **Arduino IDE:** Used for programming the microcontroller logic (C/C++).
2.  **Python:** Runs on the host computer to read Serial data and interface with the Telegram API.
3.  **Telegram Bot API:** Handles message delivery to the user's device.

### Python Libraries Required
```bash
pip install pyserial requests
```

## 🚀 Installation & Setup

### 1. Hardware Assembly

Connect the components to the Arduino Uno using the breadboard as per the **Pin Connections** table above.

### 2. Arduino Setup

1. Open the Arduino IDE.
2. Install the required libraries: `NewPing` (for Ultrasonic) and `DHT Sensor Library`.
3. Upload the `.ino` sketch to the board. The code should continuously monitor sensors and print status messages to the Serial Monitor (e.g., "Motion Detected").

### 3. Telegram Bot Setup

1. Open Telegram and search for **BotFather**.
2. Create a new bot (`/newbot`) and save the **API Token**.
3. Get your **Chat ID** (you can use a bot like `@userinfobot`).

### 4. Python Script

1. Update the Python script with your `COM_PORT` (e.g., COM3 or /dev/ttyUSB0), `BOT_TOKEN`, and `CHAT_ID`.
2. Run the script:
```bash
python telegram_alert.py
```
3. The script will listen to the Arduino via Serial. When the Arduino detects an intrusion, the Python script triggers the Telegram API to send a message.

## 🔮 Future Scope

* **Wireless Integration:** Replace USB Serial with ESP8266/ESP32 for Wi-Fi capability.
* **Camera Module:** Integrate ESP32-CAM to send photo evidence of intrusions.
* **Mobile App:** Develop a dedicated Flutter/React Native app for control.
* **AI Integration:** Use Machine Learning to reduce false positives.

## 👥 Contributors

* **Neha Santosh Yadav**
* **Kartikey Umesh Tiwari**
* **Ujjwal Suneel Tiwari**
* *Guide:* Mrs. Rashmi Maheshwari
