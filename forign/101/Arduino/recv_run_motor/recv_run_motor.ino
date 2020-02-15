#include <AccelStepper.h>
String serialData;

// Define two steppers and the pins they will use
AccelStepper stepper1(1, 2, 3);
AccelStepper stepper2(1, 4, 5);
AccelStepper stepper3(1, 6, 7);
AccelStepper stepper4(1, 8, 9);
AccelStepper stepper5(1, 10, 11);
AccelStepper stepper6(1, 42, 43);
AccelStepper stepper7(1, 26, 27);
AccelStepper stepper8(1, 24, 25);

int new_motor_00=0;
int old_motor_00=0;
int new_motor_01=0;
int old_motor_01=0;
int new_motor_02=0;
int old_motor_02=0;
int new_motor_10=0;
int old_motor_10=0;
int new_motor_11=0;
int old_motor_11=0;
int new_motor_12=0;
int old_motor_12=0;
int new_motor_20=0;
int old_motor_20=0;
int new_motor_21=0;
int old_motor_21=0;
int new_motor_22=0;
int old_motor_22=0;
int pos1;
int pos2;
int pos3;
int pos4;
int pos5;
int pos6;
int pos7;
int pos8;


void setup()
{  Serial.begin(9600); 
 stepper1.setMaxSpeed(500);
 stepper1.setAcceleration(500);
 stepper2.setMaxSpeed(500);
 stepper2.setAcceleration(500);
 stepper3.setMaxSpeed(500);
 stepper3.setAcceleration(500);
 stepper4.setMaxSpeed(500);
 stepper4.setAcceleration(500);
 stepper5.setMaxSpeed(500);
 stepper5.setAcceleration(500);
 stepper6.setMaxSpeed(500);
 stepper6.setAcceleration(500);
 stepper7.setMaxSpeed(500);
 stepper7.setAcceleration(500);
 stepper8.setMaxSpeed(500);
 stepper8.setAcceleration(500);
}

 String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void loop()
{


   if (Serial.available()>0)
  {
      serialData = Serial.readString();
 
      String motor_00_val = getValue(serialData,',',0);
      String motor_01_val = getValue(serialData,',',1);
      String motor_02_val = getValue(serialData,',',2);
      String motor_10_val = getValue(serialData,',',3);
      String motor_11_val = getValue(serialData,',',4);
      String motor_12_val = getValue(serialData,',',5);
      String motor_20_val = getValue(serialData,',',6);
      String motor_21_val = getValue(serialData,',',7);
      String motor_22_val = getValue(serialData,',',8);

     
      //Serial.print(serialData);
 
      new_motor_00 = motor_00_val.toInt();
      new_motor_01 = motor_01_val.toInt();
      new_motor_02 = motor_02_val.toInt();
      new_motor_10 = motor_10_val.toInt();
      new_motor_11 = motor_11_val.toInt();
      new_motor_12 = motor_12_val.toInt();
      new_motor_20 = motor_20_val.toInt();
      new_motor_21 = motor_21_val.toInt();

      if(old_motor_00 !=new_motor_00)
      {
         pos1=new_motor_00-old_motor_00;
          stepper1.moveTo(pos1);
        }
       else
       {
         stepper1.moveTo(pos1);
        }
      
     if(old_motor_01 !=new_motor_01)
      {
         pos2=new_motor_01-old_motor_01;
          stepper2.moveTo(pos2);
        }
       else
       {
         stepper2.moveTo(pos2);
        }

      if(old_motor_02 !=new_motor_02)
      {
         pos3=new_motor_02-old_motor_02;
          stepper3.moveTo(pos3);
        }
       else
       {
         stepper1.moveTo(pos3);
        }
        
      if(old_motor_10 !=new_motor_10)
      {
         pos4=new_motor_10-old_motor_10;
          stepper4.moveTo(pos4);
        }
       else
       {
         stepper1.moveTo(pos4);
        }
        
      if(old_motor_11 !=new_motor_11)
      {
         pos5=new_motor_11-old_motor_11;
          stepper1.moveTo(pos5);
        }
       else
       {
         stepper1.moveTo(pos5);
        }
        
      if(old_motor_12 !=new_motor_12)
      {
         pos6=new_motor_12-old_motor_12;
          stepper6.moveTo(pos6);
        }
       else
       {
         stepper1.moveTo(pos6);
        }
        
      if(old_motor_20 !=new_motor_20)
      {
         pos7=new_motor_20-old_motor_20;
          stepper7.moveTo(pos7);
        }
       else
       {
         stepper7.moveTo(pos7);
        }
        
      if(old_motor_21 !=new_motor_21)
      {
         pos8=new_motor_21-old_motor_21;
          stepper8.moveTo(pos8);
        }
       else
       {
         stepper8.moveTo(pos8);
        }
      
      
      
      
      
      Serial.print(pos1); 
      Serial.println(",");
      Serial.print(pos2);
      Serial.println(",");
      Serial.print(pos3);      

      old_motor_00=new_motor_00;
      old_motor_01=new_motor_01;
      old_motor_02=new_motor_02;
      old_motor_10=new_motor_10;
      old_motor_11=new_motor_11;
      old_motor_12=new_motor_12;
      old_motor_20=new_motor_20;
      old_motor_21=new_motor_21;
      
  while ((stepper1.distanceToGo() != 0) || (stepper2.distanceToGo() !=0) || (stepper3.distanceToGo() !=0) || (stepper4.distanceToGo() !=0) || (stepper5.distanceToGo() !=0) || 
           (stepper6.distanceToGo() !=0) || (stepper7.distanceToGo() !=0) || (stepper8.distanceToGo() !=0)) 
           {
       
            stepper1.run();
            stepper2.run();
            stepper3.run();
            stepper4.run();
            stepper5.run();
            stepper6.run();
            stepper7.run();
            stepper8.run();
  }

}


}
