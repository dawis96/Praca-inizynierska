import matplotlib.pyplot as plt
import Arduino

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