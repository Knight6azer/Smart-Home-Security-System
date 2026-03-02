import serial
import time
import requests
import sys

# ─────────────────────────────────────────────
#  CONFIGURATION  –  update these before running
# ─────────────────────────────────────────────
SERIAL_PORT = 'COM10'       # e.g. 'COM3' on Windows or '/dev/ttyUSB0' on Linux
BAUD_RATE   = 9600

# Get from @BotFather on Telegram
BOT_TOKEN   = 'YOUR_BOT_TOKEN_HERE'
# Get from @userinfobot on Telegram
CHAT_ID     = 'YOUR_CHAT_ID_HERE'

# ─────────────────────────────────────────────
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Rate-limiting: don't flood Telegram with the same alert type
ALERT_COOLDOWN = 5   # seconds between alerts of the same kind
_last_alert_times: dict = {}


def send_telegram(message: str) -> None:
    """Send a plain-text message to the configured Telegram chat."""
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
    }
    try:
        response = requests.post(TELEGRAM_API_URL, data=payload, timeout=10)
        if response.status_code == 200:
            print(f"  [Telegram ✓] {message.splitlines()[0][:60]}")
        else:
            print(f"  [Telegram ✗] {response.status_code}: {response.text[:80]}")
    except requests.exceptions.ConnectionError:
        print("  [Telegram ✗] No internet connection.")
    except Exception as e:
        print(f"  [Telegram ✗] {e}")


def send_rate_limited(alert_key: str, message: str) -> None:
    """Send a Telegram message only if the cooldown has elapsed for this alert type."""
    now = time.time()
    if now - _last_alert_times.get(alert_key, 0) >= ALERT_COOLDOWN:
        _last_alert_times[alert_key] = now
        send_telegram(message)


def process_line(line: str) -> None:
    """
    Parse a line from the Arduino Serial output and forward it to Telegram
    with the same emoji formatting visible in the working screenshots.

    Arduino messages:
      "Hello! The system is activated and everything is normal."
      "Distance: X cm  Temp: X.XX °C  Humidity: X.XX %"
      "⚠ Motion detected! Be cautious."
      "🔥 Warning: High temperature detected!"
      "🔔 Object detected within 10 cm!"
    """

    print(f"[Arduino] {line}")

    # ── Startup message ──────────────────────────────────────────────────────
    if "system is activated" in line.lower():
        send_telegram("ℹ️ Hello! The system is activated and everything is normal.")
        return

    # ── Sensor data line ─────────────────────────────────────────────────────
    if line.startswith("Distance:"):
        # Forward as-is with a coloured block emoji for readability
        send_telegram(f"🟩 {line}")
        return

    # ── PIR Motion alert ─────────────────────────────────────────────────────
    if "Motion detected" in line or "motion detected" in line:
        send_rate_limited(
            "motion",
            "🔴 Motion detected! Someone might be nearby."
        )
        return

    # ── High temperature alert ───────────────────────────────────────────────
    if "High temperature" in line or "high temperature" in line:
        send_rate_limited(
            "temp",
            "🔥 Warning: High temperature detected!"
        )
        return

    # ── Proximity / object-too-close alert ───────────────────────────────────
    if "Object detected" in line or "Proximity" in line or "too close" in line.lower():
        send_rate_limited(
            "proximity",
            "🔴 ALERT: Object too close to the sensor!"
        )
        return

    # ── Generic ALERT fallback ───────────────────────────────────────────────
    if "ALERT" in line.upper() or "ERROR" in line.upper():
        send_rate_limited("generic", f"⚠️ {line}")


def main() -> None:
    print("=" * 50)
    print("  Smart Home Security System – Monitor")
    print("=" * 50)
    print(f"  Port : {SERIAL_PORT}  |  Baud : {BAUD_RATE}")
    print(f"  Bot  : {BOT_TOKEN[:10]}…  |  Chat : {CHAT_ID}")
    print("=" * 50)

    # Send startup notification to Telegram
    send_telegram(
        "👋 Hello! Smart Security System is ACTIVE and monitoring in real-time..."
    )

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)   # wait for Arduino reset after Serial open
        print("\n[System] Connected! Listening for Arduino data…\n")

        while True:
            if ser.in_waiting > 0:
                try:
                    raw  = ser.readline()
                    line = raw.decode('utf-8', errors='replace').strip()
                    if line:
                        process_line(line)
                except UnicodeDecodeError:
                    print("[Warning] Garbled byte sequence, skipping line.")

            time.sleep(0.05)   # ~20 reads/sec, keeps CPU usage low

    except serial.SerialException as exc:
        print(f"\n[Error] Cannot open {SERIAL_PORT}.")
        print("  • Make sure the Arduino is plugged in.")
        print("  • Verify the COM port in this script.")
        print("  • Close the Arduino IDE Serial Monitor if it is open.")
        print(f"  Details: {exc}")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n[System] Stopped by user.")
        send_telegram("🔴 Smart Security System has been STOPPED.")
        if 'ser' in locals() and ser.is_open:
            ser.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
