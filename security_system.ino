/*
  Security Alarm System with Alerts
  Monitors PIR Motion Sensor, Ultrasonic Sensor, and DHT11.
  Triggers a Buzzer and sends Serial alerts for Python integration.
  
  Pin Connections:
  - Ultrasonic TRIG: D9
  - Ultrasonic ECHO: D10
  - PIR Sensor: D2
  - DHT11 Data: D7
  - Buzzer (+): D8
*/

#include <NewPing.h>
#include <DHT.h>

// --- Pin Definitions ---
#define TRIGGER_PIN  9
#define ECHO_PIN     10
#define PIR_PIN      2
#define DHT_PIN      7
#define BUZZER_PIN   8

// --- Constants & Configuration ---
#define MAX_DISTANCE 200     // Maximum distance we want to ping for (in cm). Maximum sensor distance is rated at 400-500cm.
#define ALERT_DISTANCE 10    // Distance in cm to trigger proximity alert
#define DHT_TYPE DHT11       // DHT 11

// --- Objects ---
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
DHT dht(DHT_PIN, DHT_TYPE);

// --- Variables ---
unsigned long lastTempRead = 0;
const long intervalTemp = 2000; // Read temp every 2 seconds

void setup() {
  Serial.begin(9600); // Initialize Serial for Python communication
  
  pinMode(PIR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW); // Ensure buzzer is off initially
  
  dht.begin();
  
  Serial.println("System Initialized...");
  delay(2000); // Allow sensors to stabilize
}

void loop() {
  // 1. Motion Detection (PIR)
  int pirState = digitalRead(PIR_PIN);
  if (pirState == HIGH) {
    digitalWrite(BUZZER_PIN, HIGH);
    Serial.println("ALERT: Motion Detected!");
    delay(1000); // Keep buzzer on for a bit and avoid spamming
  } else {
    digitalWrite(BUZZER_PIN, LOW);
  }

  // 2. Proximity Detection (Ultrasonic)
  unsigned int uS = sonar.ping(); 
  int distance = uS / US_ROUNDTRIP_CM; // Convert ping time to distance in cm
  
  // filtering out 0 which often means out of range or error
  if (distance > 0 && distance < ALERT_DISTANCE) {
    digitalWrite(BUZZER_PIN, HIGH);
    Serial.print("ALERT: Proximity Breach! Distance: ");
    Serial.print(distance);
    Serial.println("cm");
    delay(500); // Beep duration
  }
  // Note: If PIR is LOW but Ultrasonic is HIGH, buzzer goes LOW then HIGH quickly, creating a different pattern or sustaining the sound if loop is fast.
  
  // 3. Environmental Monitoring (DHT11)
  unsigned long currentMillis = millis();
  if (currentMillis - lastTempRead >= intervalTemp) {
    lastTempRead = currentMillis;
    
    float h = dht.readHumidity();
    float t = dht.readTemperature(); // Celsius

    if (isnan(h) || isnan(t)) {
      Serial.println("Error reading from DHT sensor!");
    } else {
      Serial.print("ENV: Humidity: ");
      Serial.print(h);
      Serial.print("%, Temp: ");
      Serial.print(t);
      Serial.println("C");
      
      // Optional: Add simple fire hazard check (e.g., Temp > 50C)
      if (t > 50) {
         digitalWrite(BUZZER_PIN, HIGH);
         Serial.println("ALERT: High Temperature Detected!");
      }
    }
  }
  
  delay(100); // Small delay for stability
}
