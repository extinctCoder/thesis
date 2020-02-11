#include <AccelStepper.h>
String serialData;

// Define two steppers and the pins they will use
AccelStepper stepper1(1, 2, 3);
AccelStepper stepper2(1, 4, 5);


int pos1 = 3600;
int pos2 = 5678;

void setup()
{  
 stepper1.setMaxSpeed(500);
 stepper1.setAcceleration(500);
 stepper2.setMaxSpeed(500);
 stepper2.setAcceleration(500);
}

void loop()
{
 if (stepper1.distanceToGo() == 0)
 {
       //pos1 = -pos1;
   stepper1.moveTo(pos1);
 }
 if (stepper2.distanceToGo() == 0)
 {
   //pos2 = -pos2;
   stepper2.moveTo(pos2);
 }
 stepper1.run();
 stepper2.run();
}
