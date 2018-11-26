import serial
import time

global connected

# class Arduino:
#     def __init__(self, com):
#         self.com = 'com'+str(com)
#         print(self.com)
#         self.arduinoSerialData = serial.Serial(self.com, 9600)
#         self.conected = 1
#         print('polaczono')
#
#     def getData(self):
#         """Pobieranie danych wysyłanych przez Arduino"""
#
#         while self.conected == 1:
#             if self.arduinoSerialData.inWaiting() > 0:
#                 self.data = self.arduinoSerialData.readline()
#                 print(self.data)
#             time.sleep(2)


def connect():
    global arduinoSerialData
    global connected
    arduinoSerialData = serial.Serial('com3', 9600)
    connected=1
    print('polaczono')


def getData():
    global connected
    global arduinoSerialData

    while connected == 1:
        if arduinoSerialData.inWaiting() > 0:
            data = str(arduinoSerialData.readline())
            arrayData=data.split(',')

            temperature=arrayData[0][4:]
            lightLevel=arrayData[2][2:]
            airHumidity=arrayData[4][3:]
            soilMoisture=arrayData[6][3:]
            #print('temperature: '+temperature+', lightLevel; '+lightLevel+', airHumidity: '+airHumidity+', soilMoisture: '+soilMoisture)
            return temperature, lightLevel, airHumidity, soilMoisture
        time.sleep(1)









