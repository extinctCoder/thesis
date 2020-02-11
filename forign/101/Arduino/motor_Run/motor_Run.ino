#include <AccelStepper.h>

// Define two steppers and the pins they will use
AccelStepper stepper1(1, 2, 3);
AccelStepper stepper2(1, 5, 6);

String recv_Data;
int new_x=0;
int old_x=0;
int new_y=0;
int old_y=0;
int x;
int y;

void setup() {
  // put your setup code here, to run once:
   //Serial.begin(9600);
    stepper1.setMaxSpeed(400);

  stepper2.setMaxSpeed(400);
  //stepper2.setAcceleration(150);
  
   stepper1.setSpeed(250);
  stepper2.setSpeed(250);
  while(true){
   stepper1.runSpeed();
   stepper2.runSpeed();
  }
}

void loop()
{
  
  
    stepper1.setSpeed(25*x);
    stepper2.setSpeed(25*y);
  // put your main code here, to run repeatedly:*/
    stepper1.runSpeed();
    stepper2.runSpeed();
 
}
