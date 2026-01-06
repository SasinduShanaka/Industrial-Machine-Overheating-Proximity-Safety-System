#define trig 2
#define echo 4
#define led 9

void setup() {
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(led, OUTPUT);

  Serial.begin(9600);
}

void loop() {

  // Trigger ultrasonic pulse
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  // Read echo time
  long t = pulseIn(echo, HIGH);

  // Convert to distance
  long cm = t / 29 / 2;
  long inches = t / 74 / 2;

  // Print distance
  Serial.print(inches);
  Serial.print(" in\t");
  Serial.print(cm);
  Serial.println(" cm");

  // LED logic
  if (cm <= 5 && cm > 0) {
    digitalWrite(led, HIGH);   // LED ON
  } else {
    digitalWrite(led, LOW);    // LED OFF
  }

  delay(200);
}
