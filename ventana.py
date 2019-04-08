#!/usr/bin/python3

import tkinter as tk
import matplotlib.pyplot as plt
from sympy import * 
import sympy as sy

ventana = tk.Tk()
x = Symbol('x')

fx = (x**2)-(6*x)+3

def busquedasIncrementales():
    ventana.withdraw()
    win = tk.Toplevel()
    win.title("Proyecto Numérico - Busquedas Incrementales")
    win.geometry('580x500')
    win.configure(background='lavender')
    plot = plt.plot(fx)
    plot.pack()
    btnOk = tk.Button(win, command = win.destroy ,text = "Cerrar")
    btnOk.pack(side = tk.BOTTOM)

def ventanaPrincipal():
    ventana.title("Proyecto Numérico")
    ventana.geometry('580x500')
    ventana.configure(background='lavender')

    btnBI = tk.Button(ventana, command=busquedasIncrementales, text = "BusquedasIncrementales")
    btnBI.pack()

    btnB = tk.Button(ventana, text = "Biseccion")
    btnB.pack()

    btnRF = tk.Button(ventana, text = "ReglaFalsa")
    btnRF.pack()

    btnPF = tk.Button(ventana, text = "PuntoFijo")
    btnPF.pack()

    ventana.mainloop()

def main():
    ventanaPrincipal()

if __name__ == "__main__":
    main()
