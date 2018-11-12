#define relay_pump 7
String recivedData = "0";

unsigned long keptTimePump=0;
unsigned long actualTimePump=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
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
   actualTimePump=millis();
   if (recivedData  == "1") {
     pumpON(9000UL, 12000UL);
  }
  if (recivedData  == "0") {
    digitalWrite(relay_pump, LOW);
  }
}

void pumpON(unsigned long startTime, unsigned long endTime){
 actualTimePump=millis();
 if (actualTimePump - keptTimePump >= startTime){
      digitalWrite(relay_pump, HIGH);
      Serial.println("1");
    }
    if (actualTimePump - keptTimePump >= endTime){
      digitalWrite(relay_pump, LOW);
      keptTimePump=actualTimePump;
      Serial.println("0");
    }
}
