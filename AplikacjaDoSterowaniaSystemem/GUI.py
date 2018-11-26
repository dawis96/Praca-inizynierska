from tkinter import *
import Arduino


class Gui:
    def __init__(self, master):
        """Interfejs Aplikacji"""
        frame = Frame(master)
        frame.grid()

        #Laczenie z Arduino
        self.label1 = Label(frame, text='Laczenie z Arduino.')
        self.label2 = Label(frame, text='COM nr:')
        self.entryNrCOM = Entry(frame)
        self.button_connect = Button(frame, text='Polacz', command=self.connect)

        self.label1.grid(row=0, columnspan=2)
        self.label2.grid(row=1)
        self.entryNrCOM.grid(row=1, column=1)
        self.button_connect.grid(row=1, column=2)

        #Sterowanie
        self.button_bulb = Button(frame, text='Wlacz Swiatlo', command=self.connect)
        self.button_fan = Button(frame, text='Wlacz wiatrak', command=self.connect)
        self.button_pump = Button(frame, text='Polacz', command=self.connect)
        self.button_servo = Button(frame, text='Polacz', command=self.connect)




    def connect(self):
        comNumber=str(self.entryNrCOM.get())
        #self.arduinoObject= Arduino(comNumber)
        Arduino.connect()






# root = Tk()
# b = Gui(root)
# root.mainloop()



