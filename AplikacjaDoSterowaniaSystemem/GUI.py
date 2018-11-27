from tkinter import * #importowanie biblioteki do tworzenia Gui
from tkinter import messagebox
import Arduino
import serial


class Gui:
    def __init__(self, master):
        """Interfejs Aplikacji"""
        frame = Frame(master)
        frame.grid()

        #Laczenie z Arduino
        self.label1 = Label(frame, text='Laczenie z Arduino:')
        self.label2 = Label(frame, text='COM nr:')
        self.entryNrCOM = Entry(frame)
        self.button_connect = Button(frame, text='Polacz', command=self.connect)

        #Odczyty z czujnikow
        self.labelEmpty = Label(frame, text='')
        self.label3 = Label(frame, text='Odczyty z czujnikow:')
        self.labelTemperature = Label(frame, text='Temperatura:')
        self.labelLightLevel = Label(frame, text='Poziom naslonecznienia:')
        self.labelAirHumidity = Label(frame, text='Wilgotnosc Powietrza:')
        self.labelSoilMoisture = Label(frame, text='Wilgotnosc gleby:')
        #zmienne to ustawiania odczytow z arduino jako tekst w polach entry
        self.textTemperature = StringVar()
        self.textLightLevel = StringVar()
        self.textAirHumidity = StringVar()
        self.textSoilMoisture = StringVar()

        self.entryTemperature = Entry(frame, state='readonly', textvariable=self.textTemperature)
        self.entryLightLevel = Entry(frame, state='readonly', textvariable=self.textLightLevel)
        self.entryAirHumidity = Entry(frame, state='readonly', textvariable=self.textAirHumidity)
        self.entrySoilMoisture = Entry(frame, state='readonly', textvariable=self.textSoilMoisture)

        # #Sterowanie
        # self.button_bulb = Button(frame, text='Wlacz Swiatlo', command=self.connect)
        # self.button_fan = Button(frame, text='Wlacz wiatrak', command=self.connect)
        # self.button_pump = Button(frame, text='Polacz', command=self.connect)
        # self.button_servo = Button(frame, text='Polacz', command=self.connect)

        # Ustawienie wszystkiego w siatce
        self.label1.grid(row=0, columnspan=2, sticky=W)
        self.label2.grid(row=1, sticky=E)
        self.entryNrCOM.grid(row=1, column=1)
        self.button_connect.grid(row=1, column=2, sticky=W)

        self.labelEmpty.grid(row=2)
        self.label3.grid(row=3, columnspan=2, sticky=W)
        self.labelTemperature.grid(row=4, sticky=E)
        self.entryTemperature.grid(row=4, column=1)
        self.labelLightLevel.grid(row=4, column=2, sticky=E)
        self.entryLightLevel.grid(row=4, column=3)
        self.labelAirHumidity.grid(row=5, column=0, sticky=E)
        self.entryAirHumidity.grid(row=5, column=1)
        self.labelSoilMoisture.grid(row=5, column=2, sticky=E)
        self.entrySoilMoisture.grid(row=5, column=3)

    def connect(self):
        comNumber = str(self.entryNrCOM.get())
        try:
            Arduino.connect(comNumber)
            self.button_connect['text'] = 'Polaczono'
            self.button_connect.config(state=DISABLED)
            self.entryNrCOM.config(state='readonly')

        except serial.serialutil.SerialException:
            messagebox.showerror("Error", "Nieprawidlowy numer COM")

# root = Tk()
# b = Gui(root)
# root.mainloop()



