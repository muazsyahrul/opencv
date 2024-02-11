const int ledPin = 13;
const int led2Pin = 12; // Change this to the pin you connect the second LED to
String msg;

void setup() {
    Serial.begin(9600);
    pinMode(ledPin, OUTPUT);
    pinMode(led2Pin, OUTPUT);
}

void loop() {
    readSerialPort();

    if (msg == "data") {
        sendData();
    } else if (msg == "led0") {
        digitalWrite(ledPin, LOW);
        digitalWrite(led2Pin, LOW);
        Serial.println("Arduino set LEDs to LOW");
    } else if (msg == "led1") {
        digitalWrite(ledPin, HIGH);
        digitalWrite(led2Pin, LOW);
        Serial.println("Arduino set led1 to HIGH");
    } else if (msg == "led2") {
        digitalWrite(ledPin, LOW);
        digitalWrite(led2Pin, HIGH);
        Serial.println("Arduino set led2 to HIGH");
    } else if (msg == "led_both") {
        digitalWrite(ledPin, HIGH);
        digitalWrite(led2Pin, HIGH);
        Serial.println("Arduino set both LEDs to HIGH");
    }

    delay(500);
}

void readSerialPort() {
    msg = "";
    if (Serial.available()) {
        delay(10);
        while (Serial.available() > 0) {
            msg += (char)Serial.read();
        }
        Serial.flush();
    }
}

void sendData() {
    Serial.print(digitalRead(ledPin));
    Serial.print("x");
    Serial.print(analogRead(A0));
    Serial.print("x");
    Serial.print(analogRead(A1));
}
