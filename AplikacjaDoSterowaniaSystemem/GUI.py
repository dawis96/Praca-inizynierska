from tkinter import * #importowanie biblioteki do tworzenia Gui
from tkinter import messagebox
import Arduino
import serial
import time


class Gui:
    controlVariable = ['0', '0', '0', '0', '0']

    def __init__(self, master):
        """Interfejs Aplikacji"""
        frame = Frame(master)
        frame.grid()

        #Laczenie z Arduino
        self.label1 = Label(frame, text='Laczenie z Arduino:')
        self.label2 = Label(frame, text='COM nr:')
        self.entryNrCOM = Entry(frame)
        self.button_connect = Button(frame, text='Polacz', width=15, command=self.connect)

        #Odczyty z czujnikow
        self.labelEmpty1 = Label(frame, text='')
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

        #Sterowanie

        self.labelEmpty2 = Label(frame, text='')
        self.label4 = Label(frame, text='Sterowanie:')
        self.radioManual = Radiobutton(frame, text='Manualne', value=2, state=DISABLED, command=self.manualMode)
        self.radioAutomatic = Radiobutton(frame, text='Automatyczne', value=1, state=DISABLED, command=self.automaticMode)
        self.button_bulb = Button(frame, text='Wlacz zarowke', width=15, state=DISABLED, command=self.bulbOnOff)
        self.button_fan = Button(frame, text='Wlacz wiatrak', width=15, state=DISABLED, command=self.fanOnOff)
        self.button_pump = Button(frame, text='Podlej', width=15, state=DISABLED, command=self.water)
        self.button_servo = Button(frame, text='Zwilz', width=15, state=DISABLED, command=self.spray)
        self.labelEmpty3 = Label(frame, text='')

        # Ustawienie wszystkiego w siatce interfejsu
        self.label1.grid(row=0, columnspan=2, sticky=W)
        self.label2.grid(row=1, sticky=E)
        self.entryNrCOM.grid(row=1, column=1)
        self.button_connect.grid(row=1, column=2)

        self.labelEmpty1.grid(row=2)
        self.label3.grid(row=3, columnspan=2, sticky=W)
        self.labelTemperature.grid(row=4, sticky=E)
        self.entryTemperature.grid(row=4, column=1)
        self.labelLightLevel.grid(row=4, column=2, sticky=E)
        self.entryLightLevel.grid(row=4, column=3)
        self.labelAirHumidity.grid(row=5, column=0, sticky=E)
        self.entryAirHumidity.grid(row=5, column=1)
        self.labelSoilMoisture.grid(row=5, column=2, sticky=E)
        self.entrySoilMoisture.grid(row=5, column=3)

        self.labelEmpty2.grid(row=6)
        self.label4.grid(row=7, sticky=W)
        self.radioAutomatic.grid(row=7, column=1)
        self.radioManual.grid(row=7, column=2)
        self.button_bulb.grid(row=8 , column=1)
        self.button_fan.grid(row=8)
        self.button_pump.grid(row=8, column=3)
        self.button_servo.grid(row=8, column=2)
        self.labelEmpty3.grid(row=9)

    def connect(self):
        """funnkcja sluzaca do polaczenia sie aplikacji z arduino"""
        comNumber = str(self.entryNrCOM.get())
        try:
            Arduino.connect(comNumber)
            self.button_connect['text'] = 'Polaczono'
            self.button_connect.config(state=DISABLED)
            self.entryNrCOM.config(state='readonly')
            self.radioAutomatic.config(state=NORMAL)
            self.radioManual.config(state=NORMAL)

        except serial.serialutil.SerialException:
            messagebox.showerror("Error", "Nieprawidlowy numer COM")

    def arduinoWrite(self):
        """Wysyłąnie zmiennych do arduino"""
        controlWrite = self.controlVariable[0] + ';' + self.controlVariable[1] + ';' + self.controlVariable[2] + ';' + \
                       self.controlVariable[3] + ';' + self.controlVariable[4]
        Arduino.arduinoSerialData.write(controlWrite.encode())

    def manualMode(self):
        """Włacznie trybu manualnego"""
        self.button_bulb.config(state=NORMAL)
        self.button_fan.config(state=NORMAL)
        self.button_pump.config(state=NORMAL)
        self.button_servo.config(state=NORMAL)
        self.controlVariable[0] = '1'

    def automaticMode(self):
        """wlaczanie trybu automatycznego"""
        self.button_bulb.config(state=DISABLED)
        self.button_fan.config(state=DISABLED)
        self.button_pump.config(state=DISABLED)
        self.button_servo.config(state=DISABLED)
        self.controlVariable = ['1', '0', '0', '0', '0']
        controlWrite = self.controlVariable[0] + ';' + self.controlVariable[1] + ';' + self.controlVariable[2] + ';' + \
                       self.controlVariable[3] + ';' + self.controlVariable[4]
        Arduino.arduinoSerialData.write(controlWrite.encode())
        self.controlVariable = ['0', '0', '0', '0', '0']
        self.arduinoWrite()

    def fanOnOff(self):
        """Sterowanie wiatrakiem z przycisku"""
        if self.controlVariable[1] == '0':
            self.controlVariable[1]='1'
            self.arduinoWrite()
            self.button_fan['text']='Wylacz wiatrak'
        elif self.controlVariable[1] == '1':
            self.controlVariable[1]='0'
            self.arduinoWrite()
            self.button_fan['text']='Wlacz wiatrak'

    def bulbOnOff(self):
        """Sterowanie zarowka z przycisku"""
        if self.controlVariable[2] == '0':
            self.controlVariable[2] = '1'
            self.arduinoWrite()
            self.button_bulb['text'] = 'Wylacz zarowke'
        elif self.controlVariable[2] == '1':
            self.controlVariable[2] = '0'
            self.arduinoWrite()
            self.button_bulb['text'] = 'Wlacz zarowke'

    def spray(self):
        """Uruchomienie serwonapedu przyciskiem"""
        self.controlVariable[4] = '1'
        self.arduinoWrite()
        time.sleep(2)
        self.controlVariable[4] = '0'
        self.arduinoWrite()

    def water(self):
        """Wlaczenie pompy na 4 sekundy w celu podlania"""
        self.controlVariable[3] = '1'
        self.arduinoWrite()
        time.sleep(3)
        self.controlVariable[3] = '0'
        self.arduinoWrite()





# root = Tk()
# b = Gui(root)
# root.mainloop()



