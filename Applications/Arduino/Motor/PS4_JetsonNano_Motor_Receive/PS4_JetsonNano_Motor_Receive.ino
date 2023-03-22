void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  while (!Serial) {
}
}

void loop() {
  char buffer[16];
  if (Serial.available() >0) {
    int size = Serial.readBytesUntil('\n', buffer,12);
    if (buffer[0] == 'F') {
        digitalWrite(2,HIGH);
        digitalWrite(3,LOW);
        digitalWrite(4,LOW);
        digitalWrite(5,LOW);

    }

    if (buffer[0] == 'B') {
       digitalWrite(3,HIGH);
       digitalWrite(2,LOW);
       digitalWrite(4,LOW);
       digitalWrite(5,LOW);
       
    }

       if (buffer[0] == 'L') {
       digitalWrite(4,HIGH);
       digitalWrite(2,LOW);
       digitalWrite(3,LOW);
       digitalWrite(5,LOW);

    }

       if (buffer[0] == 'R') {
       digitalWrite(5,HIGH);
       digitalWrite(4,LOW);
       digitalWrite(2,LOW);
       digitalWrite(3,LOW);
       
    }

       if (buffer[0] == 'S') {
       digitalWrite(5,LOW);
       digitalWrite(4,LOW);
       digitalWrite(2,LOW);
       digitalWrite(3,LOW);
       
    }
  }
}
