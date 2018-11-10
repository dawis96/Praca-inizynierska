#include "DHT.h"

#define DHT11_PIN 3
DHT dht;


#define relay_fan 2
#define relay_bulb 4
#define photoresistor A4
#define soil_moisture_sensor A0

//zmienne do pomiaru sredniej temperatury
int temperature;
int iT=0;
float sumT=0;
float meanT=0;
unsigned long keptTimeTemp=0;
//zmienne do sterowania wentylatorem
float FanOnTemp=23.0;
float FanOffTemp=22.5;

//zmienne do pomiaru sredniej wilgotnosci powietrza
int air_humidity;
int iA=0;
float sumA=0;
float meanA=0;
unsigned long keptTimeAH=0;
//zmienne do sterowania wentylatorem
float ahMin;


//zmienne do pomiaru srednigo poziomu oswietlania
int light_level;
int iL=0;
float sumL=0;
float meanL=0;
unsigned long keptTimeLight=140;
//zmienne do sterowania swiatlem
int lightMin=5;
int lightMax=40;

//zmienne do pomiaru sredniej wilgotnosci gleby
int soil_moisture;
int iS=0;
float sumS=0;
float meanS=0;
unsigned long keptTimeSoil=0;
//zmienne do sterowania wentylatorem
float smMin;


unsigned long keptTimePrint=0;//zmienna czasowa do wypisywania informacji 

unsigned long actualTime=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
unsigned long actualTime1=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis() 
unsigned long actualTime2=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
unsigned long actualTime3=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
unsigned long actualTime4=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()





void setup() {
  Serial.begin(9600);
  pinMode(relay_fan, OUTPUT) ; 
  digitalWrite(relay_fan, HIGH);
  pinMode(relay_bulb, OUTPUT) ; 
  digitalWrite(relay_bulb, HIGH);
  dht.setup(DHT11_PIN);
  

}

void loop() {
  actualTime=millis();

  meanT = average_temperature();
  meanL = average_light_level();
  meanA = average_air_humidity();
  meanS = average_soil_moisture();

  //Wypisywanie danych
  if (actualTime - keptTimePrint >= 11000UL){
    Serial.print("t:");
    Serial.print(meanT);
    Serial.print(",F:");
    if (digitalRead(relay_fan)==LOW) {
      Serial.print("1");
    }
    else {
      Serial.print("0");
    }
    Serial.print(",L:");
    Serial.print(meanL);
    Serial.print(",B:");
    if (digitalRead(relay_bulb)==LOW) {
      Serial.print("1");
    }
    else {
      Serial.print("0");
    }
    Serial.print(",AH:");
    Serial.print(meanA);
    //Wypisywanie stanu z serwa
    Serial.print(",SM:");
    Serial.println(meanS);
    //wypisywanie stanu pompy
    
    keptTimePrint= actualTime;
  }  

  //Sterowanie wentylatorem
  if (meanT>=FanOnTemp) {
    digitalWrite(relay_fan, LOW);  
  }
  else if(meanT<=FanOffTemp) {
    digitalWrite(relay_fan, HIGH);
  }

  //Sterowanie swiatlem
  if ((meanL<lightMin)||(meanL>lightMax)){
    digitalWrite(relay_bulb, HIGH);
  }
  else {
    digitalWrite(relay_bulb, LOW);
  }

  //Sterowanie serwem

  //Sterowanie pompa
  
}

float average_temperature(){
   actualTime1=millis();
   if (actualTime1 - keptTimeTemp >= 2000UL){  //odmierzanie czasu
      if (iT<10){ //robienie 10 pomiarow
      keptTimeTemp= actualTime1;
      temperature= dht.getTemperature(); //odczytywanie temperatury z czyjnika DHT11
      sumT=sumT+temperature;
      iT++;
      //Serial.print("actual temperature: ");
      //Serial.println(temperature);
     }
     else if(iT>=10){
      meanT=sumT/iT; //Obliczanie sredniej i zerowanie zmiennych
      //Serial.print("average temperature: ");
      //Serial.println(meanT);
      iT=0;
      sumT=0;
     }
  }
  return meanT;
}

float average_light_level(){
   actualTime2=millis();
   if (actualTime2 - keptTimeLight >= 1000UL){  //odmierzanie czasu
      if (iL<10){ //robienie 10 pomiarow
      keptTimeLight= actualTime2;
      light_level= map(analogRead(photoresistor), 0, 1023, 0, 99);
      sumL=sumL+light_level;
      iL++;
      //Serial.print("actual light level: ");
      //Serial.println(light_level);
     }
     else if(iL>=10){
      meanL=sumL/iL; //Obliczanie sredniej i zerowanie zmiennych
      //Serial.print("average light level: ");
      //Serial.println(meanL);
      iL=0;
      sumL=0;
     }
  }
  return meanL;
}

float average_air_humidity(){
   actualTime3=millis();
   if (actualTime1 - keptTimeAH >= 2000UL){  //odmierzanie czasu
      if (iA<10){ //robienie 10 pomiarow
      keptTimeAH= actualTime3;
      air_humidity= dht.getHumidity(); //odczytywanie temperatury z czyjnika DHT11
      sumA=sumA+air_humidity;
      iA++;
      //Serial.print("actual air humidity: ");
     // Serial.println(air_humidity);
     }
     else if(iA>=10){
      meanA=sumA/iA; //Obliczanie sredniej i zerowanie zmiennych
      //Serial.print("average air humidity: ");
      //Serial.println(meanA);
      iA=0;
      sumA=0;
     }
  }
  return meanA;
}

float average_soil_moisture(){
   actualTime4=millis();
   if (actualTime4 - keptTimeSoil >= 1000UL){  //odmierzanie czasu
      if (iS<10){ //robienie 10 pomiarow
      keptTimeSoil= actualTime4;
      soil_moisture= map(analogRead(soil_moisture_sensor), 0, 1023, 0, 99); //odczytywanie wilgotnosci gleby i zamienianie na %
      sumS=sumS+soil_moisture;
      iS++;
      //Serial.print("actual soil_moisture: ");
      //Serial.println(soil_moisture);
     }
     else if(iS>=10){
      meanS=sumS/iS; //Obliczanie sredniej i zerowanie zmiennych
     // Serial.print("average soil_moisture: ");
      //Serial.println(meanS);
      iS=0;
      sumS=0;
     }
  }
  return meanS;
}
