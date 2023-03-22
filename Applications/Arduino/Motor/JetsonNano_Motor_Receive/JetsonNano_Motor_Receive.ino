#include <AFMotor.h>

AF_DCMotor motor1(1, MOTOR12_1KHZ);
AF_DCMotor motor2(2, MOTOR12_1KHZ);
AF_DCMotor motor3(3, MOTOR34_1KHZ);
AF_DCMotor motor4(4, MOTOR34_1KHZ);

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
        //digitalWrite(LED_BUILTIN,HIGH);
        Forward();
        delay(500);
    }

    if (buffer[0] == 'B') {
       //digitalWrite(LED_BUILTIN,LOW);
       Backward();
       delay(500);
    }

       if (buffer[0] == 'L') {
       //digitalWrite(LED_BUILTIN,LOW);
       Left();
       delay(500);
    }

       if (buffer[0] == 'R') {
       //digitalWrite(LED_BUILTIN,LOW);
       Right();
       delay(500);
    }
  }

}

void Forward()
{
    motor1.run(FORWARD);
    motor1.setSpeed(90);
    motor2.run(FORWARD);
    motor2.setSpeed(90);
    motor3.run(FORWARD);
    motor3.setSpeed(90);
    motor4.run(FORWARD);
    motor4.setSpeed(90);
}

void Release()
{
    motor1.run(RELEASE);
    motor1.setSpeed(90);
    motor2.run(RELEASE);
    motor2.setSpeed(90);
    motor3.run(RELEASE);
    motor3.setSpeed(90);
    motor4.run(RELEASE);
    motor4.setSpeed(90);
}

void Backward()
{
    motor1.run(BACKWARD);
    motor1.setSpeed(90);
    motor2.run(BACKWARD);
    motor2.setSpeed(90);
    motor3.run(BACKWARD);
    motor3.setSpeed(90);
    motor4.run(BACKWARD);
    motor4.setSpeed(90);
  
}

void Right()
{
    motor1.run(FORWARD);
    motor1.setSpeed(90);
    motor2.run(BACKWARD);
    motor2.setSpeed(90);
    motor3.run(BACKWARD);
    motor3.setSpeed(90);
    motor4.run(FORWARD);
    motor4.setSpeed(90);
  
}

void Left()
{
    motor1.run(BACKWARD);
    motor1.setSpeed(90);
    motor2.run(FORWARD);
    motor2.setSpeed(90);
    motor3.run(FORWARD);
    motor3.setSpeed(90);
    motor4.run(BACKWARD);
    motor4.setSpeed(90);
}
