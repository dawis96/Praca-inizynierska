from tkinter import *
import threading
import Arduino
import GUI
import time

Arduino.connected = 0


def gui():
    global b
    root = Tk()
    b = GUI.Gui(root)
    root.mainloop()


def data():
    global b
    while True:
        try:
            dane = Arduino.getData()
            b.textTemperature.set(dane[0])
            b.textLightLevel.set(dane[1])
            b.textAirHumidity.set(dane[2])
            b.textSoilMoisture.set(dane[3])
            time.sleep(5)
        except (NameError, TypeError):
            print('brak polaczenia/dane nie sa gotowe')
            time.sleep(5)


t1 = threading.Thread(target=gui)
t2 = threading.Thread(target=data)

t1.start()
t2.start()

t1.join()
t2.join()