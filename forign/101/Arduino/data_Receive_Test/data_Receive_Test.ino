String serialData;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available())
  {
      serialData = Serial.readString();
      //Serial.print(serialData);
      String yval= serialData.substring(0,1);
      String zval= serialData.substring(2,3);
      int y_val= yval.toInt();
      int z_val =zval.toInt();
      if (y_val == 1)
    {
        Serial.print(y_val);
        digitalWrite(13,HIGH);}
      //else{
        //digitalWrite(13,LOW);
      }
  
}
