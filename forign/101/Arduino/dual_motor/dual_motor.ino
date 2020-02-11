#include <AccelStepper.h>

//AccelStepper Xaxis(1, 2, 5); // pin 2 = step, pin 5 = direction
//AccelStepper Yaxis(1, 3, 6); // pin 3 = step, pin 6 = direction
//AccelStepper Zaxis(1, 4, 7); // pin 4 = step, pin 7 = direction
int x=45;
AccelStepper Xaxis(1, 2, 3); // pin 3 = step, pin 6 = direction
AccelStepper Yaxis(1, 5, 6); // pin 4 = step, pin 7 = direction
 // pin 5 = step, pin 8 = direction

void setup() {
  Xaxis.setMaxSpeed(400);
  Yaxis.setMaxSpeed(400);
  
  
  
}

void loop() {  
  Xaxis.setSpeed(x*25);
  Yaxis.setSpeed(250);
   Xaxis.runSpeed();
   Yaxis.runSpeed();
}
