import matplotlib.pyplot as plt
import Arduino
import pandas as pd


def plotSubplot(a):

    plt.subplot(2, 2, 1)
    plt.plot( Arduino.temperatureArray[a:], 'r.-')
    plt.title('Temperatura')
    plt.ylabel('°C')

    plt.subplot(2, 2, 2)
    plt.plot( Arduino.lightLevelArray[a:], 'y.-')
    plt.title('Nasłonecznienie')
    plt.ylabel('%')

    plt.subplot(2, 2, 3)
    plt.plot(Arduino.airHumidityArray[a:], 'b.-')
    plt.title('Wilgotność powietrza')
    plt.xlabel('nr pomiaru')
    plt.ylabel('%')

    plt.subplot(2, 2, 4)
    plt.plot(Arduino.soilMoistureArray[a:], 'g.-')
    plt.title('Wilgotność gleby')
    plt.xlabel('nr pomiaru')
    plt.ylabel('%')
    plt.show()

def dataframe(type):
    frame={'Czas': Arduino.timeArray[2:],
           'Temperatura': Arduino.temperatureArray[2:],
           'Naslonecznienie': Arduino.lightLevelArray[2:],
           'Wilgotnosc powietrza': Arduino.airHumidityArray[2:],
           'Wilgotnosc gleby': Arduino.soilMoistureArray[2:],
           'Wiatrak': Arduino.fanConditionArray[2:],
           'Zarowka': Arduino.bulbConditionArray[2:],
           'Serwonapęd': Arduino.servoConditionArray[2:],
           'Pompa': Arduino.pumpConditionArray[2:],
           'Tryb': Arduino.modeConditionArray[2:]
           }
    df = pd.DataFrame.from_dict(frame)

    if type == 'xlsx':
        writer = pd.ExcelWriter('bonsai'+Arduino.timeArray[2][:10]+'.'+str(type))
        df.to_excel(writer, 'Sheet1')
        writer.save()

    if type == 'csv':
        df.to_csv('bonsai.'+str(type))
