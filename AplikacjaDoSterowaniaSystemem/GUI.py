from __future__ import unicode_literals
from tkinter import * #importowanie biblioteki do tworzenia Gui
from tkinter import messagebox, ttk
import serial
import time
import sys

import arduino
import analizaDanych

class Gui:
    controlVariable = ['0', '0', '0', '0', '0']

    def __init__(self, master):
        """Interfejs Aplikacji"""
        frame = Frame(master)
        frame.grid()

        #Laczenie z Arduino
        self.label1 = Label(frame, text='Łączenie z Arduino:')
        self.label2 = Label(frame, text='COM nr:')
        self.entryNrCOM = ttk.Entry(frame)
        self.button_connect = ttk.Button(frame, text='Polącz', width=22, command=self.connect)

        #Odczyty z czujnikow
        self.labelEmpty1 = Label(frame, text='')
        self.label3 = Label(frame, text='Odczyty z czujników:')
        self.labelTemperature = Label(frame, text='Temperatura:')
        self.labelLightLevel = Label(frame, text='Poziom nasłonecznienia:')
        self.labelAirHumidity = Label(frame, text='Wilgotność powietrza:')
        self.labelSoilMoisture = Label(frame, text='Wilgotność gleby:')

        #zmienne to ustawiania odczytow z arduino jako tekst w polach entry
        self.textTemperature = StringVar()
        self.textLightLevel = StringVar()
        self.textAirHumidity = StringVar()
        self.textSoilMoisture = StringVar()

        self.entryTemperature = ttk.Entry(frame, state='readonly', textvariable=self.textTemperature)
        self.entryLightLevel =ttk.Entry(frame, state='readonly', textvariable=self.textLightLevel)
        self.entryAirHumidity = ttk.Entry(frame, state='readonly', textvariable=self.textAirHumidity)
        self.entrySoilMoisture = ttk.Entry(frame, state='readonly', textvariable=self.textSoilMoisture)

        #Sterowanie
        self.labelEmpty2 = Label(frame, text='')
        self.label4 = Label(frame, text='Sterowanie:')
        self.radioManual = Radiobutton(frame, text='Manualne', value=2, state=DISABLED, command=self.manualMode)
        self.radioAutomatic = Radiobutton(frame, text='Automatyczne', value=1, state=DISABLED,
                                              command=self.automaticMode)
        self.radioAutomatic.select()
        self.button_bulb = ttk.Button(frame, text='Włącz żarówkę', width=22, state=DISABLED, command=self.bulbOnOff)
        self.button_fan = ttk.Button(frame, text='Włącz wiatrak', width=22, state=DISABLED, command=self.fanOnOff)
        self.button_pump = ttk.Button(frame, text='Podlej', width=22, state=DISABLED, command=self.water)
        self.button_servo = ttk.Button(frame, text='Zwilż', width=22, state=DISABLED, command=self.spray)
        self.labelEmpty3 = Label(frame, text='')

        # Analiza danych
        self.textTime = StringVar()
        self.textDataCount = StringVar()

        self.label5 = Label(frame, text='Analiza danych:')
        self.label6 = Label(frame, text='Zapisywanie danych od:')
        self.entryTime = ttk.Entry(frame, state='readonly', textvariable=self.textTime)
        self.Label7 = Label(frame, text='Liczba wpisów:')
        self.entryDataCount = ttk.Entry(frame, state='readonly', textvariable=self.textDataCount)
        self.Label8 = Label(frame, text='Wygeneruj:')
        self.button_1hourplot = ttk.Button(frame, text='Wykres ostatniej godziny', width=22, state=DISABLED,
                                           command=self.plot1hour)
        self.button_plot = ttk.Button(frame, text='Wykres z calego zakresu', width=22, state=DISABLED,
                                      command=lambda: analizaDanych.plotSubplot(2))
        self.button_excel = ttk.Button(frame, text='Plik Excel', width=22, state=DISABLED,
                                       command=lambda: analizaDanych.dataframe('xlsx'))
        self.button_csv = ttk.Button(frame, text='Plik csv', width=22, state=DISABLED,
                                     command=lambda: analizaDanych.dataframe('csv'))
        self.labelEmpty4 = Label(frame, text='')

        #Wyjscie, informacje
        self.button_info = ttk.Button(frame, text='Info', width=45, command=self.info)
        self.button_quit = ttk.Button(frame, text='Wyjście', width=45, command=self.onExit)
        #self.protocol("WM_DELETE_WINDOW", self.onExit)

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

        self.label5.grid(row=10, columnspan=2, sticky=W)
        self.label6.grid(row=11, sticky=E)
        self.entryTime.grid(row=11, column=1)
        self.Label7.grid(row=11, column=2, sticky=E)
        self.entryDataCount.grid(row=11, column=3)
        self.Label8.grid(row=12, column=1, columnspan=2)
        self.button_1hourplot.grid(row=13, column=0)
        self.button_plot.grid(row=13, column=1)
        self.button_excel.grid(row=13, column=2)
        self.button_csv.grid(row=13, column=3)
        self.labelEmpty4.grid(row=14)

        self.button_info.grid(row=15, column=0, columnspan=2)
        self.button_quit.grid(row=15, column=2, columnspan=2)

    def connect(self):
        """funnkcja sluzaca do wywolania funkcji laczacej sie z arduino oraz odblokowania przyciskow po polaczeniu."""
        comNumber = str(self.entryNrCOM.get())
        try:
            arduino.connect(comNumber)
            self.button_connect['text'] = 'Polączono'
            self.button_connect.config(state=DISABLED)
            self.entryNrCOM.config(state='readonly')
            self.radioAutomatic.config(state=NORMAL)
            self.radioManual.config(state=NORMAL)
            self.button_1hourplot.config(state=NORMAL)
            self.button_plot.config(state=NORMAL)
            self.button_excel.config(state=NORMAL)
            self.button_csv.config(state=NORMAL)
            self.automaticMode()


        except serial.serialutil.SerialException:
            messagebox.showerror("Error", "Nieprawidłowy numer COM")

    def arduinoWrite(self):
        """Wysyłąnie zmiennych sterujacych do arduino"""
        controlWrite = self.controlVariable[0] + ';' + self.controlVariable[1] + ';' + self.controlVariable[2] + ';' + \
                       self.controlVariable[3] + ';' + self.controlVariable[4]
        arduino.arduinoSerialData.write(controlWrite.encode())

    def manualMode(self):
        """Włacznie trybu manualnego"""
        self.button_bulb.config(state=NORMAL)
        self.button_fan.config(state=NORMAL)
        self.button_pump.config(state=NORMAL)
        self.button_servo.config(state=NORMAL)
        self.controlVariable[0] = '1'
        self.arduinoWrite()

    def automaticMode(self):
        """wlaczanie trybu automatycznego"""
        self.button_bulb.config(state=DISABLED)
        self.button_fan.config(state=DISABLED)
        self.button_pump.config(state=DISABLED)
        self.button_servo.config(state=DISABLED)
        #self.controlVariable = ['1', '0', '0', '0', '0']
        #self.arduinoWrite()
        #time.sleep(0.5)
        self.controlVariable[0] = '0'
        self.arduinoWrite()

    def fanOnOff(self):
        """Sterowanie wiatrakiem z przycisku"""
        if self.controlVariable[1] == '0':
            self.controlVariable[1]='1'
            self.arduinoWrite()
            self.button_fan['text']='Wyłącz wiatrak'
        elif self.controlVariable[1] == '1':
            self.controlVariable[1]='0'
            self.arduinoWrite()
            self.button_fan['text']='Włącz wiatrak'

    def bulbOnOff(self):
        """Sterowanie zarowka z przycisku"""
        if self.controlVariable[2] == '0':
            self.controlVariable[2] = '1'
            self.arduinoWrite()
            self.button_bulb['text'] = 'Wyłącz żarówkę'
        elif self.controlVariable[2] == '1':
            self.controlVariable[2] = '0'
            self.arduinoWrite()
            self.button_bulb['text'] = 'Włącz żarówkę'

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

    def plot1hour(self):
        """Wygenerowanie wykresu z ostatniej godziny"""
        if len(arduino.airHumidityArray) < 62:
            messagebox.showwarning("Error", "Niewystarczająca ilość zebranych danych")
        else:
            analizaDanych.plotSubplot(-60)

    def info(self):
        """Funkcja pokazujaca informacjie o aplikacji"""
        messagebox.showinfo("Informacje", "Część pracy inżynierskiej pt. 'System automatyzacji uprawy drzewka bonsai'" +
        ". Aplikacja służy do zarządzania oraz sterowania systemem a także do zbierania danych." +
        "Wykonał Damian Grzywna.")

    def onExit(self):
        """Potwierdzenie wyjscia oraz zamkniecie calej aplkacji"""
        if messagebox.askyesno("Wyjście", "Czy na pewno chcesz wyjść?"):
            arduino.connected = 2
            sys.exit()