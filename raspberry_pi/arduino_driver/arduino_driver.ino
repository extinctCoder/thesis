#include <AccelStepper.h>
String motor_data = "";
bool data_filled = false;

AccelStepper stepper_00(AccelStepper::DRIVER, 2, 3); //AccelStepper::DRIVER, STEPPER1_STEP_PIN, STEPPER1_DIR_PIN
AccelStepper stepper_01(AccelStepper::DRIVER, 4, 5);
AccelStepper stepper_02(AccelStepper::DRIVER, 6, 7);
AccelStepper stepper_10(AccelStepper::DRIVER, 8, 9);
AccelStepper stepper_11(AccelStepper::DRIVER, 10, 11);
AccelStepper stepper_12(AccelStepper::DRIVER, 42, 43);
AccelStepper stepper_20(AccelStepper::DRIVER, 26, 27);
AccelStepper stepper_21(AccelStepper::DRIVER, 24, 25);
AccelStepper stepper_22(AccelStepper::DRIVER, 24, 25);

String string_block(String data, char separator, int index);

void setup()
{
  Serial.begin(9600);
  
  stepper_00.setMaxSpeed(250);
  stepper_00.setAcceleration(250);
  
  stepper_01.setMaxSpeed(250);
  stepper_01.setAcceleration(250);
  
  stepper_02.setMaxSpeed(250);
  stepper_02.setAcceleration(250);
  
  stepper_10.setMaxSpeed(250);
  stepper_10.setAcceleration(250);

  stepper_11.setMaxSpeed(250);
  stepper_11.setAcceleration(250);

  stepper_12.setMaxSpeed(250);
  stepper_12.setAcceleration(250);
  
  stepper_20.setMaxSpeed(250);
  stepper_20.setAcceleration(250);

  stepper_21.setMaxSpeed(250);
  stepper_21.setAcceleration(250);

  stepper_22.setMaxSpeed(250);
  stepper_22.setAcceleration(250);

  stepper_00.setCurrentPosition(0);
  stepper_01.setCurrentPosition(0);
  stepper_02.setCurrentPosition(0);
  stepper_10.setCurrentPosition(0);
  stepper_11.setCurrentPosition(0);
  stepper_12.setCurrentPosition(0);
  stepper_20.setCurrentPosition(0);
  stepper_21.setCurrentPosition(0);
  stepper_22.setCurrentPosition(0);
  
  stepper_00.setMaxSpeed(250);
  stepper_00.setAcceleration(250);
  
  stepper_01.setMaxSpeed(250);
  stepper_01.setAcceleration(250);
  
  stepper_02.setMaxSpeed(250);
  stepper_02.setAcceleration(250);
  
  stepper_10.setMaxSpeed(250);
  stepper_10.setAcceleration(250);

  stepper_11.setMaxSpeed(250);
  stepper_11.setAcceleration(250);

  stepper_12.setMaxSpeed(250);
  stepper_12.setAcceleration(250);
  
  stepper_20.setMaxSpeed(250);
  stepper_20.setAcceleration(250);

  stepper_21.setMaxSpeed(250);
  stepper_21.setAcceleration(250);

  stepper_22.setMaxSpeed(250);
  stepper_22.setAcceleration(250);

  Serial.println("arduino is waiting for command");
}


void loop()
{
  while (!Serial.available()){
    motor_data = "";
    data_filled = false;
  }
  while (Serial.available()){
    if (Serial.available() >0)
    {
      char motor_char = Serial.read();
      motor_data += motor_char; 
      data_filled = true;
    }
  }

  if(!Serial.available() && data_filled){
    stepper_00.moveTo(string_block(motor_data,',',0).toInt());
    stepper_01.moveTo(string_block(motor_data,',',1).toInt());
    stepper_02.moveTo(string_block(motor_data,',',2).toInt());
    stepper_10.moveTo(string_block(motor_data,',',3).toInt());
    stepper_11.moveTo(string_block(motor_data,',',4).toInt());
    stepper_12.moveTo(string_block(motor_data,',',5).toInt());
    stepper_20.moveTo(string_block(motor_data,',',6).toInt());
    stepper_21.moveTo(string_block(motor_data,',',7).toInt());
    stepper_22.moveTo(string_block(motor_data,',',8).toInt());

    while(stepper_00.distanceToGo() != 0 || stepper_01.distanceToGo() != 0 || stepper_02.distanceToGo() != 0 || 
          stepper_10.distanceToGo() != 0 || stepper_11.distanceToGo() != 0 || stepper_12.distanceToGo() != 0 || 
          stepper_20.distanceToGo() != 0 || stepper_21.distanceToGo() != 0 || stepper_22.distanceToGo() != 0){
      if(stepper_00.distanceToGo() != 0){
        stepper_00.run();
        }
      if(stepper_01.distanceToGo() != 0){
        stepper_01.run();
        }
      if(stepper_02.distanceToGo() != 0){
        stepper_02.run();
        }
      if(stepper_10.distanceToGo() != 0){
        stepper_10.run();
        }
      if(stepper_11.distanceToGo() != 0){
        stepper_11.run();
        }
      if(stepper_12.distanceToGo() != 0){
        stepper_12.run();
        }
      if(stepper_20.distanceToGo() != 0){
        stepper_20.run();
        }
      if(stepper_21.distanceToGo() != 0){
        stepper_21.run();
        }
      if(stepper_22.distanceToGo() != 0){
        stepper_22.run();
        }
      }
    }
}

String string_block(String data, char separator, int block_index)
{
  int found = 0;
  int str_index[] = { 0, -1 };
  int maximum_index = data.length() - 1;

  for (int i = 0; i <= maximum_index && found <= block_index; i++) {
      if (data.charAt(i) == separator || i == maximum_index) {
          found++;
          str_index[0] = str_index[1] + 1;
          str_index[1] = (i == maximum_index) ? i+1 : i;
      }
  }
    return found > block_index ? data.substring(str_index[0], str_index[1]) : "";
}
