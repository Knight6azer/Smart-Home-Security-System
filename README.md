# Smart Home Security System 🚨

![Arduino](https://img.shields.io/badge/Hardware-Arduino_Uno-blue)
![Python](https://img.shields.io/badge/Software-Python_3.x-yellow)
![Telegram](https://img.shields.io/badge/Alerts-Telegram_Bot-2CA5E0)
![IoT](https://img.shields.io/badge/Tech-IoT_Security-green)

## 📖 Abstract
A real-time, low-cost smart security system built on **Arduino Uno** that monitors motion, proximity, temperature, and humidity. On detecting a threat, it triggers a local **buzzer** and simultaneously sends **instant notifications to a Telegram Bot** via a Python bridge script — keeping you informed from anywhere.

---

## ✨ Features
| Feature | Sensor | Threshold |
|---|---|---|
| **Motion Detection** | PIR (HC-SR501) | Any movement |
| **Proximity Alert** | Ultrasonic (HC-SR04) | Object < 10 cm |
| **High Temperature Warning** | DHT11 | Temp > 33 °C |
| **Humidity Monitoring** | DHT11 | Continuous |
| **Real-Time Telegram Alerts** | — | All events |
| **Local Buzzer Alarm** | Active Buzzer | Motion / Proximity |

---

## 🛠️ Hardware Requirements
- Arduino Uno (ATmega328P)
- HC-SR04 Ultrasonic Sensor
- HC-SR501 PIR Motion Sensor
- DHT11 Temperature & Humidity Sensor
- Active Buzzer
- Breadboard + Jumper Wires
- USB Type-A to Type-B cable (Arduino ↔ PC)

---

## 🔌 Pin Connections
| Component | Pin | Arduino Pin |
|---|---|---|
| HC-SR04 | TRIG | D9 |
| HC-SR04 | ECHO | D10 |
| PIR Sensor | OUT | D2 |
| DHT11 | DATA | D7 |
| Active Buzzer | (+) | D8 |
| All sensors | VCC / GND | 5V / GND |

---

## 💻 Software Stack
- **Arduino IDE** — uploads the `.ino` sketch to the board
- **Python 3.x** — bridges Serial data → Telegram API
- **Telegram Bot API** — delivers real-time alerts to your phone

### Python Dependencies
```bash
pip install pyserial requests
```

---

## 🚀 Setup & Usage

### 1 · Hardware
Wire all components to the Arduino Uno as per the pin table above.

### 2 · Arduino Sketch
1. Open **`security_system.ino`** in the Arduino IDE.
2. Install the **DHT sensor library** (by Adafruit) via the Library Manager.
3. Select **Board → Arduino Uno** and the correct **COM port**.
4. Upload the sketch.

**Expected Serial Monitor output (9600 baud):**
```
Hello! The system is activated and everything is normal.
Distance: 2272 cm  Temp: 33.70 °C  Humidity: 57.00 %
🔥 Warning: High temperature detected!
⚠ Motion detected! Be cautious.
🔔 Object detected within 10 cm!
```

### 3 · Telegram Bot
1. Open Telegram → search **@BotFather** → `/newbot` → copy the **API Token**.
2. Search **@userinfobot** → copy your **Chat ID**.

### 4 · Python Script
1. Open **`telegram_alert.py`** and fill in:
   ```python
   SERIAL_PORT = 'COM10'          # your Arduino port
   BOT_TOKEN   = 'YOUR_TOKEN'
   CHAT_ID     = 'YOUR_CHAT_ID'
   ```
2. Run:
   ```bash
   python telegram_alert.py
   ```

**Telegram bot messages sent:**
```
👋 Hello! Smart Security System is ACTIVE and monitoring in real-time...
ℹ️ Hello! The system is activated and everything is normal.
🟩 Distance: 2271 cm  Temp: 33.60 °C  Humidity: 56.00 %
🔥 Warning: High temperature detected!
🔴 Motion detected! Someone might be nearby.
🔴 ALERT: Object too close to the sensor!
```

---

## 🔮 Future Scope
- Replace USB Serial with **ESP8266/ESP32** for wireless operation
- Add **ESP32-CAM** to send photo snapshots on intrusion
- Build a dedicated **mobile app** (Flutter / React Native)
- Use **ML** to reduce false positives

---

## 👥 Contributors
- **Neha Santosh Yadav**
- **Kartikey Umesh Tiwari**
- **Ujjwal Suneel Tiwari**
- *Guide:* Mrs. Rashmi Maheshwari
