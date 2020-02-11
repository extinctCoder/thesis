#include <AccelStepper.h>
String serialData;

// Define two steppers and the pins they will use
AccelStepper stepper1(1, 2, 3);
AccelStepper stepper2(1, 4, 5);

int new_x=0;
int old_x=0;
int new_y=0;
int old_y=0;
int pos1;
int pos2;

void setup()
{  Serial.begin(9600); 
 stepper1.setMaxSpeed(500);
 stepper1.setAcceleration(500);
 stepper2.setMaxSpeed(500);
 stepper2.setAcceleration(500);
}

void loop()
{
   if (Serial.available()>0)
  {
      serialData = Serial.readString();
      String xval;
      String yval;
      //Serial.print(serialData);
      for (int i = 0; i < serialData.length(); i++) {
             if (serialData.substring(i, i+1) == ",") {
                   xval = serialData.substring(0, i);
                   yval= serialData.substring(i+1);
                   break;
  }
}
 
      new_x= xval.toInt();
      new_y =yval.toInt();
      pos1=new_x-old_x;
      pos2=new_y-old_y;
      old_x=new_x;
      old_y=new_y;
       Serial.print(pos1);
      Serial.println(",");
      Serial.print(pos2);
      Serial.println(",");
      stepper1.moveTo(pos1);
      stepper2.moveTo(pos2);
  while ((stepper1.distanceToGo() != 0) || (stepper2.distanceToGo() !=0)) {
       //pos1 = -pos1;
   

 
   //pos2 = -pos2;
   
    stepper1.run();
    stepper2.run();
  }

}


}
