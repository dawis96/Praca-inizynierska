#include <Servo.h>
String recivedData = "0";
Servo servomotor;

unsigned long keptTimeServo=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
unsigned long actualTimeServo=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
int a=0;

void setup() {
  Serial.begin(9600);
  servomotor.attach(9);
}

void loop() {

   if(Serial.available() > 0){
     recivedData = Serial.readStringUntil('\n'); 
   }
   
   if (recivedData  == "1") {
    servoMove(2000UL, 12000UL);
    }
   if (recivedData  == "0") {
    servomotor.write(0);
  }
}

void servoMove(unsigned long startTime, unsigned long endTime){
  actualTimeServo=millis();
  if (actualTimeServo - keptTimeServo >= startTime){
      servomotor.write(0);
    }
    if (actualTimeServo - keptTimeServo >= endTime){
      servomotor.write(120);
      keptTimeServo=actualTimeServo;
      Serial.println("Move");
    }
}
