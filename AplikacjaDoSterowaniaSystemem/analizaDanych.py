import matplotlib.pyplot as plt
import pandas as pd

import arduino


def plotSubplot(a):
    """Funkcja generujaca wykresy z zebranych danych"""

    plt.subplot(2, 2, 1)
    plt.plot( arduino.temperatureArray[a:], 'r.-')
    plt.title('Temperatura')
    plt.ylabel('°C')

    plt.subplot(2, 2, 2)
    plt.plot(arduino.lightLevelArray[a:], 'y.-')
    plt.title('Nasłonecznienie')
    plt.ylabel('%')

    plt.subplot(2, 2, 3)
    plt.plot(arduino.airHumidityArray[a:], 'b.-')
    plt.title('Wilgotność powietrza')
    plt.xlabel('nr pomiaru')
    plt.ylabel('%')

    plt.subplot(2, 2, 4)
    plt.plot(arduino.soilMoistureArray[a:], 'g.-')
    plt.title('Wilgotność gleby')
    plt.xlabel('nr pomiaru')
    plt.ylabel('%')
    plt.show()

def dataframe(type):
    """Funkcja do generowania plikow xlsx lub csv z zebranych danych"""

    frame = {'Czas': arduino.timeArray[2:],
            'Temperatura (°C)': arduino.temperatureArray[2:],
            'Naslonecznienie (%)': arduino.lightLevelArray[2:],
            'Wilgotnosc powietrza (%)': arduino.airHumidityArray[2:],
            'Wilgotnosc gleby (%)': arduino.soilMoistureArray[2:],
            'Wiatrak': arduino.fanConditionArray[2:],
            'Zarowka': arduino.bulbConditionArray[2:],
            'Serwonaped': arduino.servoConditionArray[2:],
            'Pompa': arduino.pumpConditionArray[2:],
            'Tryb': arduino.modeConditionArray[2:]}

    df = pd.DataFrame.from_dict(frame)
    try:
        if type == 'xlsx': #tworzenie pliku Excel
            writer = pd.ExcelWriter('bonsai'+arduino.timeArray[2][:10]+'.'+str(type))
            df.to_excel(writer, 'Sheet1')
            writer.save()

        if type == 'csv': #tworzenie pliku csv
            df.to_csv('bonsai'+arduino.timeArray[2][:10]+'.'+str(type))
    except IndexError:
        pass