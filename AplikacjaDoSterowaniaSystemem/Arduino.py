import serial #biblioteka do komunikacji z portem szeregowym
import time

def connect(comNumber):
    """Funckja do polaczenia się aplikacji z Arduino"""
    global arduinoSerialData
    global connected
    com = 'com'+comNumber
    arduinoSerialData = serial.Serial(com, 9600)
    connected = 1 #zmienna rozpoczynajaca odbieranie danych w funkci getData()
    print('polaczono') #tekst pomocniczy w konsoli


def getData():
    """Odczytywanie danych z arduino i podzielenie ich na poszczegolne zmienne"""
    global connected
    global arduinoSerialData

    while connected == 1: #Jesli jestesmy polaczeni z arduino
        if arduinoSerialData.inWaiting() > 0:
            data = str(arduinoSerialData.readline())
            arrayData = data.split(',')
            temperature = arrayData[0][4:]
            lightLevel = arrayData[2][2:]
            airHumidity = arrayData[4][3:]
            soilMoisture = arrayData[6][3:]
            #print('temperature: '+temperature+', lightLevel; '+lightLevel+', airHumidity: '+airHumidity+', soilMoisture: '+soilMoisture)
            return temperature, lightLevel, airHumidity, soilMoisture
        time.sleep(1)









