#include <DHT.h>

#define DHTPIN 7
#define DHTTYPE DHT11

#define trig 2
#define echo 4
#define led 9     // Distance LED
#define ledt 11   // Temperature LED

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(led, OUTPUT);
  pinMode(ledt, OUTPUT);   // ✅ FIX 1

  Serial.begin(9600);
  dht.begin();
}

void loop() {

  // 🌡 Temperature reading
  float temperature = dht.readTemperature();

  if (isnan(temperature)) {
    Serial.println("Failed to read DHT sensor");
  } else {
    Serial.print("Temp: ");
    Serial.print(temperature);
    Serial.println(" °C");

    // 🔥 Temperature LED logic
    if (temperature > 29.0) {
      digitalWrite(ledt, HIGH);
    } else {
      digitalWrite(ledt, LOW);
    }
  }

  delay(1000);  // DHT needs delay

  // 📡 Ultrasonic trigger
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  long t = pulseIn(echo, HIGH);

  long cm = t / 29 / 2;

  Serial.print("Distance: ");
  Serial.print(cm);
  Serial.println(" cm");

  // 💡 Distance LED logic
  if (cm <= 5 && cm > 0) {
    digitalWrite(led, HIGH);
  } else {
    digitalWrite(led, LOW);
  }

  delay(500);
}
