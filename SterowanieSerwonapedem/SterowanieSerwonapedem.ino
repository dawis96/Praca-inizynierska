#include <Servo.h>
String recivedData = "0";
Servo servomotor;

unsigned long keptTimeServo1=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
unsigned long keptTimeServo2=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
unsigned long actualTime2=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
int a=0;
void setup() {
  Serial.begin(9600);
  servomotor.attach(9);
}

void loop() {

   if(Serial.available() > 0){
     recivedData = Serial.readStringUntil('\n'); 
   }
   actualTime2=millis();
   if (recivedData  == "1") {
    if (actualTime2 - keptTimeServo1 >= 2000UL){
      servomotor.write(0);
      keptTimeServo1=actualTime2;
      Serial.println("0");
    }
    if (actualTime2 - keptTimeServo2 >= 12000UL){
      servomotor.write(120);
      keptTimeServo2=actualTime2;
      Serial.println("120");
    }
  }
  if (recivedData  == "0") {
    servomotor.write(0);
  }
}
