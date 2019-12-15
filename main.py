from tkinter import *
from tkinter import ttk

from calculator import WIDTHBTN, HEIGHTBTN, Calculator


class MainApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Calculadora')
        self.geometry("{}x{}".format(WIDTHBTN*4, HEIGHTBTN*6))
        
        c = Calculator(self)
        c.pack()

    def start(self):
        self.mainloop()
    

if __name__ == '__main__':
    app = MainApp()
    app.start()
