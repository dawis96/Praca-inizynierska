from tkinter import *
import threading
import Arduino
import GUI
import time

Arduino.connected=0

def gui():
    root = Tk()
    b = GUI.Gui(root)
    root.mainloop()


def data():
    while True:
        dane = Arduino.getData()
        print(dane)
        time.sleep(5)
t2=threading.Thread(target=gui)
t1=threading.Thread(target=data)

t1.start()
t2.start()

t1.join()
t2.join()