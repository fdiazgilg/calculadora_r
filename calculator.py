from tkinter import *
from tkinter import ttk
from romannumber import *

SELWIDHT = 50
HEIGHTBTN = 50
WIDTHBTN = 68


def openParenthesis(cadena):
    nP = 0
    for caracter in cadena:
        if caracter == '(':
            nP +=1
        if caracter == ')':
            nP -=1
    return nP


class CalcButton(ttk.Frame):
    def __init__(self, parent, text, command, wbtn=1, hbtn=1):
        ttk.Frame.__init__(self, parent, width=wbtn*WIDTHBTN, height=hbtn*HEIGHTBTN)

        self.pack_propagate(0)

        s = ttk.Style()
        s.theme_use('alt')
        s.configure('my.TButton', foreground='black', font=('Helvetica', '11', 'bold'))

        self.__b = ttk.Button(self, style='my.TButton', text=text, command=command)
        self.__b.pack(side=TOP, fill=BOTH, expand=True)


class Display(ttk.Frame):
    cadena = '_'

    def __init__(self, parent):
        ttk.Frame.__init__(self,parent, width=4*WIDTHBTN, height=HEIGHTBTN)

        self.pack_propagate(0)

        s = ttk.Style()
        s.theme_use('alt')
        s.configure('my.TLabel', font="Helvetica 25")

        self.__lbl = ttk.Label(self, text=self.cadena, style='my.TLabel', anchor=E, background='black', foreground='white')
        self.__lbl.pack(side=TOP, fill=BOTH, expand=True)
    
    def mostrar(self, cadena):
        self.cadena = str(cadena)
        self.__lbl.config(text=self.cadena)


class Selector(ttk.Frame):
    tipus = 'R'
    def __init__(self, parent, command, tipus='R'):
        ttk.Frame.__init__(self, parent, width=SELWIDHT, height=HEIGHTBTN)

        self.pack_propagate(0)
        self.tipus = tipus
        self.command = command

        self.value = StringVar()
        self.value.trace("w", self.selected)

        self.value.set(self.tipus)

        self.__rbR = ttk.Radiobutton(self, text='Rom', value='R', variable=self.value, command=lambda: command('R'))
        self.__rbA = ttk.Radiobutton(self, text='Arab', value='A', variable=self.value, command=lambda: command('A'))
        self.__rbR.place(x=0, y=2)
        self.__rbA.place(x=0, y=25)
    
    def selected(self, *args):
        self.command(self.value.get())


class Calculator(ttk.Frame):
    op1 = None
    operacion = None
    op2 = None

    cadena = ''
    __maxnumbers = 12

    def __createLayoutArabic(self):
        layoutArabic = ttk.Frame(self, name='layoutArabic')
        CalcButton(layoutArabic, text= 'C', command=self.clear).grid(column=0, row=0)
        CalcButton(layoutArabic, text= '+/-', command=self.negar).grid(column=1, row=0)
        CalcButton(layoutArabic, text= '%', command=lambda: self.operar('%')).grid(column=2, row=0)

        CalcButton(layoutArabic, text='÷', command=lambda: self.operar('÷')).grid(column=3, row=0)
        CalcButton(layoutArabic, text='7', command=lambda: self.addChar('7')).grid(column=0, row=2)
        CalcButton(layoutArabic, text='8', command=lambda: self.addChar('8')).grid(column=1, row=2)
        CalcButton(layoutArabic, text='9', command=lambda: self.addChar('9')).grid(column=2, row=2)
        CalcButton(layoutArabic, text='x', command=lambda: self.operar('x')).grid(column=3, row=2)

        CalcButton(layoutArabic, text='4', command=lambda: self.addChar('4')).grid(column=0, row=3)
        CalcButton(layoutArabic, text='5', command=lambda: self.addChar('5')).grid(column=1, row=3)
        CalcButton(layoutArabic, text='6', command=lambda: self.addChar('6')).grid(column=2, row=3)
        CalcButton(layoutArabic, text='-', command=lambda: self.operar('-')).grid(column=3, row=3)

        CalcButton(layoutArabic, text='1', command=lambda: self.addChar('1')).grid(column=0, row=4)
        CalcButton(layoutArabic, text='2', command=lambda: self.addChar('2')).grid(column=1, row=4)
        CalcButton(layoutArabic, text='3', command=lambda: self.addChar('3')).grid(column=2, row=4)
        CalcButton(layoutArabic, text='+', command=lambda: self.operar('+')).grid(column=3, row=4)

        CalcButton(layoutArabic, text='0', command=lambda: self.addChar('0')).grid(column=1, row=5, columnspan=1)
        CalcButton(layoutArabic, text=',', command=lambda: self.addChar(',')).grid(column=2, row=5)
        CalcButton(layoutArabic, text='=', command=lambda: self.operar('=')).grid(column=3, row=5)
        
        return layoutArabic

    def __createLayoutRoman(self):
        layoutRoman = ttk.Frame(self, name='layoutRoman')
        self.buttonAC = CalcButton(layoutRoman, text="CE", command=self.clear, wbtn=3)
        self.buttonAC.grid(column=0, row=1, columnspan=3)
        self.buttonDiv = CalcButton(layoutRoman, text="÷", command=lambda: self.operar('÷'))
        self.buttonDiv.grid(column=3, row=1)

        self.buttonC = CalcButton(layoutRoman, text="C", command=lambda: self.addChar('C'))
        self.buttonC.grid(column=0, row=2)
        self.buttonD = CalcButton(layoutRoman, text="D", command=lambda: self.addChar('D'))
        self.buttonD.grid(column=1, row=2)
        self.buttonM = CalcButton(layoutRoman, text="M", command=lambda: self.addChar('M'))
        self.buttonM.grid(column=2, row=2)
        self.buttonMul = CalcButton(layoutRoman, text="x", command=lambda: self.operar('x'))
        self.buttonMul.grid(column=3, row=2)

        self.buttonX = CalcButton(layoutRoman, text="X", command=lambda: self.addChar('X'))
        self.buttonX.grid(column=0, row=3)
        self.buttonL = CalcButton(layoutRoman, text="L", command=lambda: self.addChar('L'))
        self.buttonL.grid(column=1, row=3)
        self.buttonPi = CalcButton(layoutRoman, text="(", command=lambda: self.addChar('('))
        self.buttonPi.grid(column=2, row=3)
        self.buttonSub = CalcButton(layoutRoman, text="-", command=lambda: self.operar('-'))
        self.buttonSub.grid(column=3, row=3)
        
        self.buttonI = CalcButton(layoutRoman, text="I", command=lambda: self.addChar('I'))
        self.buttonI.grid(column=0, row=4)
        self.buttonV = CalcButton(layoutRoman, text="V", command=lambda: self.addChar('V'))
        self.buttonV.grid(column=1, row=4)
        self.buttonPr = CalcButton(layoutRoman, text=")", command=lambda: self.addChar(')'))
        self.buttonPr.grid(column=2, row=4)
        self.buttonAdd = CalcButton(layoutRoman, text="+", command=lambda: self.operar('+'))
        self.buttonAdd.grid(column=3, row=4)

        self.buttonEqu = CalcButton(layoutRoman, text="=", command=lambda: self.operar('='), wbtn=2)
        self.buttonEqu.grid(column=2, row=5, columnspan=2)

        return layoutRoman


    def __init__(self, parent, modo='R'):
        ttk.Frame.__init__(self, parent)

        self.modo = modo
        
        self.pantalla = Display(self)
        self.pantalla.grid(column=0, row=0, columnspan=4)

        self.layoutRoman = self.__createLayoutRoman()
        self.layoutArabic= self.__createLayoutArabic()

        self.selector = Selector(self, command=self.eligeModo, tipus=self.modo)
        self.selector.grid(column=0, row=5, columnspan=1, sticky=W+S, padx=5)

    def formatArabic(self, resultado):
        resultado = str(resultado).replace('.', ',')
        resultado = resultado.rstrip('0')
        if resultado[-1] == ',':
            resultado = resultado[:-1]
        return resultado


    def negar(self):
        candidato = self.pantalla.cadena.replace(',', '.')
        if candidato != '0':
            resultado = -float(candidato)
            resultado = self.formatArabic(resultado)
        self.pantalla.mostrar(resultado)


    def operar(self,operacion):
        if operacion in ('+','-','x','÷'):
            if self.modo == 'R':
                self.op1 = RomanNumber(self.pantalla.cadena)
            if self.modo == 'A':
                candidato = self.pantalla.cadena.replace(',', '.')
                self.op1 = float(candidato)

            self.operacion = operacion
            self.clear()
        
        elif operacion == '%' and self.operacion in ('+','-','x','÷'):
            if self.modo == 'A':
                candidato = self.pantalla.cadena.replace(',', '.')
                self.op2 = float(candidato)
            
            if self.operacion == '+':
                resultado = self.op1 + (self.op1 * self.op2) / 100
            
            if self.operacion == '-':
                resultado = self.op1 - (self.op1 * self.op2) / 100
            
            if self.operacion == 'x':
                resultado = (self.op1 * self.op2) / 100

            if self.operacion == '÷':
                try:
                    resultado = self.op1 / (self.op2 / 100)
                except ZeroDivisionError:
                    return 0
            
            if self.modo == 'A' and resultado != 0:
                resultado = "{0:.4f}".format(resultado)
                resultado = self.formatArabic(resultado)

            self.pantalla.mostrar(resultado)
            self.cadena = ''



        elif operacion == '=':
            if self.modo == 'R':
                self.op2 = RomanNumber(self.pantalla.cadena)
            if self.modo == 'A':
                candidato = self.pantalla.cadena.replace(',', '.')
                self.op2 = float(candidato)

            if self.operacion == '+':
                resultado = self.op1 + self.op2
            
            if self.operacion == '-':
                resultado = self.op1 - self.op2
            
            if self.operacion == 'x':
                resultado = self.op1 * self.op2
            
            if self.operacion == '÷':
                if self.modo == 'A':
                    try:
                        resultado = self.op1 / self.op2
                    except ZeroDivisionError:
                        return 0
                if self.modo == 'R':
                    resultado = self.op1 / self.op2

            if self.modo == 'A':
                resultado = "{0:.4f}".format(resultado)
                resultado = self.formatArabic(resultado)
           
            self.pantalla.mostrar(resultado)
            self.cadena = ''


    def eligeModo(self, modo):
        self.modo = modo

        if modo == 'R':
            self.layoutArabic.grid_forget()
            self.layoutRoman.grid(column=0, row=1, columnspan=4, rowspan=5)
            self.clear()


        elif modo == 'A':
            self.layoutRoman.grid_forget()
            self.layoutArabic.grid(column=0, row=1, columnspan=4, rowspan=5)
            self.clear()

    def clear(self):
        if self.modo == 'R':
            self.cadena = '_'

        if self.modo == 'A':
            self.cadena = '0'
        
        self.pantalla.mostrar(self.cadena)
    

    def addChar(self, caracter):

        if len(self.cadena) >= self.__maxnumbers:
            return
        
        if self.modo == 'R':
            if self.cadena == '_':
                self.cadena = ''
            self.cadena += caracter

            try:
                nr = RomanNumber(self.cadena)
            except ValueError:
                self.cadena = self.cadena[:-1]
            except IndexError:
                pass
            
        

        if self.modo == 'A':
            if self.cadena == '0':
                if caracter == ',':
                    self.cadena += caracter
                else:
                    self.cadena = ''
            self.cadena += caracter
        
            try:
                candidato = self.cadena.replace(',', '.')
                na = float(candidato)
            
            except ValueError:
                self.cadena = self.cadena[:-1]

        self.pantalla.mostrar(self.cadena)
