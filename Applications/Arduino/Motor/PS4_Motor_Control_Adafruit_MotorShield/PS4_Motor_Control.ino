#include <Wire.h>
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

Adafruit_DCMotor *Motor1 = AFMS.getMotor(1);
Adafruit_DCMotor *Motor2 = AFMS.getMotor(2);
Adafruit_DCMotor *Motor3 = AFMS.getMotor(3);
Adafruit_DCMotor *Motor4 = AFMS.getMotor(4);

int defaultSpeed = 90;

void setup() {
  Serial.begin(9600);
  AFMS.begin();
  Motor1 -> setSpeed(defaultSpeed);
  Motor2 -> setSpeed(defaultSpeed);
  Motor3 -> setSpeed(defaultSpeed);
  Motor4 -> setSpeed(defaultSpeed);
  pinMode(LED_BUILTIN, OUTPUT);
  while (!Serial) {
}
}

void loop() {
  char buffer[16];
  if (Serial.available() >0) {
    int size = Serial.readBytesUntil('\n', buffer,12);
    if (buffer[0] == 'F' ) {Forward();}
    if (buffer[0] == 'B' ) {Backward();}
    if (buffer[0] == 'X') {RotateLeft();}
    if (buffer[0] == 'Z') {RotateRight();}
    if (buffer[0] == 'L' ) {SideLeft();}
    if (buffer[0] == 'R' ) {SideRight();}
    if (buffer[0] == 'S' ) {Release();}
    if (buffer[0] == 'Q' ) {SlowRotateLeft();}
  }
}

void Backward(){
  Motor1 -> run(FORWARD);
  Motor2 -> run(BACKWARD);
  Motor3 -> run(BACKWARD);
  Motor4 -> run(FORWARD); 
}

void Forward(){
  Motor1 -> run(BACKWARD);
  Motor2 -> run(FORWARD);
  Motor3 -> run(FORWARD);
  Motor4 -> run(BACKWARD); 
}

void Release(){
  Motor1 -> run(RELEASE);
  Motor2 -> run(RELEASE);
  Motor3 -> run(RELEASE);
  Motor4 -> run(RELEASE); 
}

void RotateLeft() {
  Motor1 -> run(FORWARD);
  Motor2 -> run(FORWARD);
  Motor3 -> run(FORWARD);
  Motor4 -> run(FORWARD); 
}

void RotateRight() {
  Motor1 -> run(BACKWARD);
  Motor2 -> run(BACKWARD);
  Motor3 -> run(BACKWARD);
  Motor4 -> run(BACKWARD); 
}

void SideLeft() {
  Motor1 -> setSpeed(140);
  Motor2 -> setSpeed(140);
  Motor3 -> setSpeed(140);
  Motor4 -> setSpeed(140);
  
  Motor1 -> run(FORWARD);
  Motor2 -> run(FORWARD);
  Motor3 -> run(BACKWARD);
  Motor4 -> run(BACKWARD); 
  
}

void SideRight() {
  Motor1 -> setSpeed(140);
  Motor2 -> setSpeed(140);
  Motor3 -> setSpeed(140);
  Motor4 -> setSpeed(140);
  
  Motor1 -> run(BACKWARD);
  Motor2 -> run(BACKWARD);
  Motor3 -> run(FORWARD);
  Motor4 -> run(FORWARD); 
}

void SlowRotateLeft() {
  Motor1 -> setSpeed(50);
  Motor2 -> setSpeed(50);
  Motor3 -> setSpeed(50);
  Motor4 -> setSpeed(50);
  
  Motor1 -> run(FORWARD);
  Motor2 -> run(FORWARD);
  Motor3 -> run(FORWARD);
  Motor4 -> run(FORWARD);
  
}
