#define relay_pump 7
String recivedData = "0";

unsigned long keptTimePump1=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
unsigned long keptTimePump2=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
unsigned long keptTimePump3=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
unsigned long actualTime2=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
int a=0;
void setup() {
  Serial.begin(9600);
  pinMode(relay_pump, OUTPUT) ; 
  digitalWrite(relay_pump, LOW);
}

void loop() {

   if(Serial.available() > 0){
     recivedData = Serial.readStringUntil('\n'); 
   }
   actualTime2=millis();
   if (recivedData  == "1") {
    if (actualTime2 - keptTimePump1 >= 9000UL){
      digitalWrite(relay_pump, HIGH);
      //keptTimePump1=actualTime2;
      Serial.println("1");

      
    }
    if (actualTime2 - keptTimePump1 >= 12000UL){
      digitalWrite(relay_pump, LOW);
      keptTimePump1=actualTime2;
      Serial.println("0");
    }
  }
  if (recivedData  == "0") {
    digitalWrite(relay_pump, LOW);
  }
}
