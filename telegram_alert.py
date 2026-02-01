import serial
import time
import requests
import sys

# --- CONFIGURATION (UPDATE THESE) ---
# Replace 'COM3' with your Arduino's port (e.g., 'COM3', '/dev/ttyUSB0')
SERIAL_PORT = 'COM3' 
BAUD_RATE = 9600

# Telegram Bot Credentials
# 1. Search for @BotFather on Telegram to get a token.
# 2. Search for @userinfobot to get your chat ID.
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
CHAT_ID = 'YOUR_CHAT_ID_HERE'

# API URL
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_telegram_alert(message):
    """Component to send a message to the Telegram user."""
    payload = {
        'chat_id': CHAT_ID,
        'text': f"🚨 SECURITY ALERT 🚨\n\n{message}"
    }
    
    try:
        response = requests.post(TELEGRAM_API_URL, data=payload)
        if response.status_code == 200:
            print(f"[Sent] Telegram: {message}")
        else:
            print(f"[Error] Telegram API: {response.text}")
    except Exception as e:
        print(f"[Error] Network: {e}")

def main():
    print("--- IoT Security Alarm System ---")
    print(f"Connecting to {SERIAL_PORT} at {BAUD_RATE} baud...")
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        # Allow Arduino to reset after connection
        time.sleep(2) 
        print("Connected! Listening for alerts...\n")
        
        while True:
            if ser.in_waiting > 0:
                try:
                    # Read line from Serial and decode
                    line = ser.readline().decode('utf-8').strip()
                    
                    if line:
                        print(f"[Arduino] {line}")
                        
                        # Check for specific alert keywords from Arduino code
                        if "ALERT" in line:
                            # Send the whole line as the alert message
                            send_telegram_alert(line)
                            
                        # Optional: Add rate limiting or filtering if needed
                        
                except UnicodeDecodeError:
                    print("[Warning] Received garbage data, skipping...")
                    
            time.sleep(0.1) # Prevent high CPU usage
            
    except serial.SerialException as e:
        print(f"\n[Error] Could not connect to {SERIAL_PORT}.")
        print("1. Check if Arduino is plugged in.")
        print("2. Verify the Port name in the script.")
        print("3. Close the Arduino IDE Serial Monitor if it's open.")
        print(f"Details: {e}")
    except KeyboardInterrupt:
        print("\n\nExiting...")
        if 'ser' in locals() and ser.is_open:
            ser.close()
        sys.exit()

if __name__ == "__main__":
    main()
