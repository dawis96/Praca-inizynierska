#include <Servo.h> #Biblioteka do obsługi serwonapędu
#include "DHT.h" #Biblioteka do odczytywania wartości z czujnika temperatury
//Zdefiniowanie pinów
#define DHT11_PIN 3
DHT dht;
#define photoresistor A4
#define soil_moisture_sensor A0
#define relay_fan 2
#define relay_bulb 4
#define relay_pump 7
Servo servomotor;

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
//zmienne do sterowania serwonapedem
float ahMin=90;

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
//zmienne do sterowania pompa
float smMin=10.0;

unsigned long keptTimePrint=0;//zmienna czasowa do wypisywania informacji 
unsigned long actualTime=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
unsigned long actualTime1=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis() 
unsigned long actualTime2=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
unsigned long actualTime3=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
unsigned long actualTime4=0;//zmienna czasowa do zapisywania aktualnczego czasu funkcja millis()
unsigned long keptTimePump=0;
unsigned long actualTimePump=0;
unsigned long keptTimeP=0;
unsigned long keptTimeServo=0;
unsigned long actualTimeServo=0;

String recivedData; //Zmienna do sterowania recznego
int writeServo, writePump; //zmienne do wysylania stanu serwa i pompy
String mode;

void setup() {
  Serial.begin(9600);
  pinMode(relay_fan, OUTPUT) ; 
  digitalWrite(relay_fan, HIGH);
  pinMode(relay_bulb, OUTPUT) ; 
  digitalWrite(relay_bulb, HIGH);
  pinMode(relay_pump, OUTPUT) ; 
  digitalWrite(relay_pump, HIGH); //narazie LOW, po podlaczeniu przekaznika zmienić na HIGH
  dht.setup(DHT11_PIN);
  servomotor.attach(9);
  servomotor.write(0);
  mode = "0";
}

void loop() {
  actualTime=millis();

  meanT = average_temperature();
  meanL = average_light_level();
  meanA = average_air_humidity();
  meanS = average_soil_moisture();

  //Odczytywanie danych do sterowania recznego
  if(Serial.available() > 0){
     recivedData = Serial.readStringUntil('\n'); 
      mode = getValue(recivedData,';',0); //trybreczny-1, automatczyny-0
   }
   String manualLight= getValue(recivedData,';',1); //1-zarowka wlaczona 0- zarowka wylaczona
   String manualFan = getValue(recivedData,';',2); 
   String manualPump = getValue(recivedData,';',3);
   String manualServo = getValue(recivedData,';',4);

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
    Serial.print(",S:");
     if (writeServo == 1){
      Serial.print("1");
      writeServo = 0;
     }
     else{
      Serial.print("0");
     }
    Serial.print(",SM:");
    Serial.print(meanS);
    Serial.print(",P:");
    if (writePump == 1) {
      Serial.print("1");
      writePump = 0;
    }
    else {
      Serial.print("0");
    }
    Serial.print(",M:");
    if (mode=="1") {
      Serial.println("M");
    }
    else {
      Serial.println("A");
    }
    keptTimePrint= actualTime;
  }  

  //Sterowanie manualne:
  if (mode=="1") {
    //Sterowanie wentylatorem
    if (manualFan=="1") {
      digitalWrite(relay_fan, LOW);  
    }
    else {
      digitalWrite(relay_fan, HIGH);
    }
    //Sterowanie swiatlem
    if (manualLight == "1"){
      digitalWrite(relay_bulb, LOW);
    }
    else {
    digitalWrite(relay_bulb, HIGH);
    }
    //Sterowanie serwonapedem
    if (manualServo=="1"){
      servoMove(1000UL, 2000UL);
      writeServo = 1;
    }
    else{
      servomotor.write(0);
    }
    //Sterowanie pompy
    if (manualPump=="1") {
      pumpON(500UL, 4500UL);
      writePump = 1;
    }
    else{
      digitalWrite(relay_pump, HIGH);
    }
  }
  else {
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
    //Sterowanie serwonapedem
    if (meanA<ahMin){
      servoMove(2000UL, 12000UL);
      writeServo = 1;
    }
    else{
      servomotor.write(0);
    }

    //Sterowanie pompy
    if (meanS<smMin) {
     pumpON(9000UL, 12000UL);
     writePump = 1;
    }
    else{
      digitalWrite(relay_pump, HIGH);
    } 
  }
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

void pumpON(unsigned long startTime, unsigned long endTime){
 actualTimePump=millis();
 if (actualTimePump - keptTimePump >= startTime){
      digitalWrite(relay_pump, LOW);
    }
    if (actualTimePump - keptTimePump >= endTime){
      digitalWrite(relay_pump, HIGH);
      keptTimePump=actualTimePump;
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
      
      //Serial.println("Move");
    }
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}
