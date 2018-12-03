import serial #biblioteka do komunikacji z portem szeregowym
import time #bibliotek do zarzadzania czasem
from time import strftime, localtime #bibliotek do pobierania aktualnego czasu

global arduinoSerialData, timeArray, temperatureArray, fanConditionArray, lightLevelArray, bulbConditionArray, \
                airHumidityArray, servoConditionArray, soilMoistureArray, pumpConditionArray, modeConditionArray
timeArray = []
temperatureArray = []
fanConditionArray = []
lightLevelArray = []
bulbConditionArray= []
airHumidityArray = []
servoConditionArray = []
soilMoistureArray = []
pumpConditionArray = []
modeConditionArray = []


def connect(comNumber):
    """Funckja do polaczenia się aplikacji z Arduino"""
    global arduinoSerialData, connected
    com = 'com'+comNumber
    arduinoSerialData = serial.Serial(com, 9600)
    connected = 1 #zmienna rozpoczynajaca odbieranie danych w funkci getData()
    #print('polaczono') #pomocniczy komunikat


def getData():
    """Odczytywanie wiersza przychodzacego z arduino i podzielenie ich na poszczegolne zmienne oraz zapisywanie odczytow
        do list"""
    global connected
    global arduinoSerialData

    while connected == 1: #Jesli jestesmy polaczeni z arduino
        if arduinoSerialData.inWaiting() > 0:
            data = str(arduinoSerialData.readline())
            actualTime= strftime("%Y-%m-%d %H:%M:%S", localtime())
            arrayData = data.split(',')
            temperature = arrayData[0][4:]
            fanCondition = arrayData[1][2]
            lightLevel = arrayData[2][2:]
            bulbCondition=arrayData[3][2]
            airHumidity = arrayData[4][3:]
            servoCondition = arrayData[5][2]
            soilMoisture = arrayData[6][3:]
            pumpCondition = arrayData[7][2]
            modeCondition = arrayData[8][2]

            #Zapisywanie danych do list
            global timeArray, temperatureArray, fanConditionArray, lightLevelArray, bulbConditionArray, \
                airHumidityArray, servoConditionArray, soilMoistureArray, pumpConditionArray, modeConditionArray
            timeArray.append(actualTime)
            temperatureArray.append(float(temperature))
            fanConditionArray.append(int(fanCondition))
            lightLevelArray.append(float(lightLevel))
            bulbConditionArray.append(int(bulbCondition))
            airHumidityArray.append(float(airHumidity))
            servoConditionArray.append(int(servoCondition))
            soilMoistureArray.append(float(soilMoisture))
            pumpConditionArray.append(int(pumpCondition))
            modeConditionArray.append(modeCondition)

            return temperature, lightLevel, airHumidity, soilMoisture, timeArray, temperatureArray, fanConditionArray, lightLevelArray, \
                bulbConditionArray, airHumidityArray, servoConditionArray, soilMoistureArray, pumpConditionArray, \
                modeConditionArray
