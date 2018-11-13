#dziala z programem arduino 'SterowanieReczne'

import serial
import time

arduinoSerialData = serial.Serial('com3', 9600)


while True:
    dane = input('tryb;swiatlo;wentylator;pompa;servo')  # 1-wlaczone 0-wylaczone
    arduinoSerialData.write(dane.encode())
    time.sleep(5)


    if arduinoSerialData.inWaiting() > 0 :
        myData=arduinoSerialData.readline()

        print(myData)
        print(dane)
    #dane = dane[:6] + "0;0"
    #arduinoSerialData.write(dane.encode())
