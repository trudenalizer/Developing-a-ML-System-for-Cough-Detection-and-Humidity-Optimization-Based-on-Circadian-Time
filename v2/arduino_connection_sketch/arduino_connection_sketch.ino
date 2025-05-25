#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT22
#define RELAY_PIN 3
#define SOUND_PIN A0  // MAX4466 microphone OUT pin

DHT dht(DHTPIN, DHTTYPE);

// Cough detection threshold
const int COUGH_THRESHOLD = 550;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);
  delay(2000);
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Read sound level
  int rawSound = analogRead(SOUND_PIN);
  float soundVoltage = (rawSound / 1023.0) * 5.0;

  // SNR guess: normalized sound level (for approx.)
  float snr = rawSound / 10.0;

  // Cough detection
  int cough = rawSound > COUGH_THRESHOLD ? 1 : 0;

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("error,error,error,error,error");
  } else {
    // Expected data from Python side: temp, humidity, snr, ses, cough
    Serial.print(temperature, 2);
    Serial.print(",");
    Serial.print(humidity, 2);
    Serial.print(",");
    Serial.print(snr, 2);
    Serial.print(",");
    Serial.print(soundVoltage, 2);
    Serial.print(",");
    Serial.println(cough);
    Serial.flush(); 
    delay(10);
  }

  // Check relay depending on Python's response
  if (Serial.available() > 0) {
    String incomingData = Serial.readStringUntil('\n');
    incomingData.trim();
    if (incomingData == "1") {
      digitalWrite(RELAY_PIN, HIGH);
      Serial.println("Relay=ON");
    } else if (incomingData == "0") {
      digitalWrite(RELAY_PIN, LOW);
      Serial.println("Relay=OFF");
    }
  }

  delay(2000);
}