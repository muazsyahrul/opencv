int led1Pin = 13;  // LED 1 connected to pin 13
int led2Pin = 12;  // LED 2 connected to pin 12

void setup() {
  Serial.begin(9600);
  pinMode(led1Pin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    switch (command) {
      case 'L':
        digitalWrite(led1Pin, HIGH);  // Turn on LED 1
        digitalWrite(led2Pin, LOW);   // Turn off LED 2
        break;
      case 'R':
        digitalWrite(led1Pin, LOW);   // Turn off LED 1
        digitalWrite(led2Pin, HIGH);  // Turn on LED 2
        break;
      case 'C':
        digitalWrite(led1Pin, HIGH);  // Turn on LED 1
        digitalWrite(led2Pin, HIGH);  // Turn on LED 2
        break;
      case 'O':
        digitalWrite(led1Pin, LOW);   // Turn off LED 1
        digitalWrite(led2Pin, LOW);   // Turn off LED 2
        break;
    }
  }
}
