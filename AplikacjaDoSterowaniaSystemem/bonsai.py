from tkinter import *
import threading
import time

import arduino
import gui

arduino.connected = 0


def interfejs():
    """Funkcja tworzaca obiekt klasy Gui"""
    global b, root
    root = Tk()

    b = gui.Gui(root)
    root.title('bonsai.py')
    root.iconbitmap(r'bonsai.ico') #Designed by Freepik from www.flaticon.com
    root.mainloop()


def data():
    """funkcja wywoluje jesli to mozliwe funkcje getData z pliku arduino oraz wysyla dane z czujnikow do interfejsu"""
    global b
    while True:
        try:
            dane = arduino.getData()
            b.textTemperature.set(dane[0]+'°C')
            b.textLightLevel.set(dane[1]+'%')
            b.textAirHumidity.set(dane[2]+'%')
            b.textSoilMoisture.set(dane[3]+'%')
            try:
                b.textTime.set(dane[4][2])
            except IndexError:
                pass
            if len(dane[4])-2 > 0:
                b.textDataCount.set(len(dane[4])-2)
            time.sleep(5)
        except (NameError, TypeError):
            #print('brak polaczenia/dane nie sa gotowe')
            time.sleep(2)
        if arduino.connected == 2:
            break


t1 = threading.Thread(target=interfejs)
t2 = threading.Thread(target=data)

t1.start()
t2.start()

t1.join()
t2.join()
