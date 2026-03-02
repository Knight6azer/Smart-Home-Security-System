/*
  Smart Home Security System
  Monitors PIR Motion Sensor, Ultrasonic Sensor (HC-SR04), and DHT11.
  Triggers a Buzzer and sends structured Serial messages for Python/Telegram integration.

  Pin Connections:
  - Ultrasonic TRIG : D9
  - Ultrasonic ECHO : D10
  - PIR Sensor      : D2
  - DHT11 Data      : D7
  - Buzzer (+)      : D8
*/

#include <DHT.h>

// --- Pin Definitions ---
#define TRIGGER_PIN  9
#define ECHO_PIN     10
#define PIR_PIN      2
#define DHT_PIN      7
#define BUZZER_PIN   8

// --- Constants & Configuration ---
#define ALERT_DISTANCE 10    // Distance in cm to trigger proximity alert
#define TEMP_THRESHOLD 33.0  // Temperature threshold (°C) to trigger heat warning
#define DHT_TYPE DHT11

// --- Sensor Object ---
DHT dht(DHT_PIN, DHT_TYPE);

// --- Timing Variables ---
unsigned long lastReadTime   = 0;
const long    readInterval   = 1000; // Print sensor data every 1 second

// --- Helper: Measure distance using HC-SR04 (no library) ---
long measureDistance() {
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // 30 ms timeout (~500 cm)
  long distance = duration / 58;                  // convert to cm
  return distance;
}

void setup() {
  Serial.begin(9600);

  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN,    INPUT);
  pinMode(PIR_PIN,     INPUT);
  pinMode(BUZZER_PIN,  OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  dht.begin();
  delay(2000); // Allow sensors to stabilise

  Serial.println("Hello! The system is activated and everything is normal.");
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - lastReadTime >= readInterval) {
    lastReadTime = currentMillis;

    // --- 1. Read DHT11 ---
    float humidity    = dht.readHumidity();
    float temperature = dht.readTemperature();

    // --- 2. Read Ultrasonic ---
    long distance = measureDistance();

    // --- 3. Read PIR ---
    int pirState = digitalRead(PIR_PIN);

    // --- 4. Print main data line ---
    if (!isnan(humidity) && !isnan(temperature)) {
      Serial.print("Distance: ");
      Serial.print(distance);
      Serial.print(" cm  Temp: ");
      Serial.print(temperature, 2);
      Serial.print(" \xB0");   // degree symbol
      Serial.print("C  Humidity: ");
      Serial.print(humidity, 2);
      Serial.println(" %");
    } else {
      Serial.println("Error: DHT sensor read failed!");
    }

    // --- 5. PIR Alert ---
    if (pirState == HIGH) {
      Serial.println("⚠ Motion detected! Be cautious.");
      digitalWrite(BUZZER_PIN, HIGH);
      delay(500);
      digitalWrite(BUZZER_PIN, LOW);
    }

    // --- 6. Temperature Alert ---
    if (!isnan(temperature) && temperature > TEMP_THRESHOLD) {
      Serial.println("🔥 Warning: High temperature detected!");
    }

    // --- 7. Proximity Alert ---
    if (distance > 0 && distance < ALERT_DISTANCE) {
      Serial.println("🔔 Object detected within 10 cm!");
      digitalWrite(BUZZER_PIN, HIGH);
      delay(300);
      digitalWrite(BUZZER_PIN, LOW);
    }
  }
}
