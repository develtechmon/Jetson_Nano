#include <AFMotor.h>

AF_DCMotor motor1(1, MOTOR12_1KHZ);
AF_DCMotor motor2(2, MOTOR12_1KHZ);
AF_DCMotor motor3(3, MOTOR34_64KHZ);
AF_DCMotor motor4(4, MOTOR34_64KHZ);


void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
   // Forward();
   // delay(500); 
   // Backward();
   // delay(500);
   // Release();
   // delay(800);
    
    //Right();
    //delay(800);
   // Left();
    //delay(800);
    //Release();
    //delay(800);
    SlideRight();
    delay(2000);
    SlideLeft();
    delay(2000);
    //Release();
    //delay(1000);

}

void Forward()
{
    motor1.run(FORWARD);
    motor1.setSpeed(130);
    motor2.run(FORWARD);
    motor2.setSpeed(130);
    motor3.run(FORWARD);
    motor3.setSpeed(130);
    motor4.run(FORWARD);
    motor4.setSpeed(130);
}

void Release()
{
    motor1.run(RELEASE);
    motor1.setSpeed(130);
    motor2.run(RELEASE);
    motor2.setSpeed(130);
    motor3.run(RELEASE);
    motor3.setSpeed(130);
    motor4.run(RELEASE);
    motor4.setSpeed(130);
}

void Backward()
{
    motor1.run(BACKWARD);
    motor1.setSpeed(130);
    motor2.run(BACKWARD);
    motor2.setSpeed(130);
    motor3.run(BACKWARD);
    motor3.setSpeed(130);
    motor4.run(BACKWARD);
    motor4.setSpeed(130);
  
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

void SlideRight()
{
    motor1.run(BACKWARD);
    motor1.setSpeed(180);
    motor2.run(FORWARD);
    motor2.setSpeed(180);
    motor3.run(BACKWARD);
    motor3.setSpeed(180);
    motor4.run(FORWARD);
    motor4.setSpeed(180);
}

void SlideLeft()
{
    motor1.run(FORWARD);
    motor1.setSpeed(180);
    motor2.run(BACKWARD);
    motor2.setSpeed(180);
    motor3.run(FORWARD);
    motor3.setSpeed(180);
    motor4.run(BACKWARD);
    motor4.setSpeed(180);
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
