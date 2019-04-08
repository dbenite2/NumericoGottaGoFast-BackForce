#!/usr/bin/python3

from sympy import * 
import sympy as sy
import numpy as np
import math

x0 = 0
tol = 0
ite = 0
fx = 0
lista = []

x = Symbol('x')

def llamadasSistema():
    global x0, ite, tol
    x0 = float(input('Introduce un X0: '))
    tol = float(input('Introduce una tolerancia: '))
    ite = int(input('Introduce un Número de Iteraciones: '))

def busquedas():
    global x0, tol, ite

    fx0 = funcionF(x0)
    dfx0 = funcionFP(x0)
    error = tol + 1
    contador = 0
    print('{:30},{:30},{:30},{:30},{:30}'.format('n','xn','f(xn)','d(xn)','error'))

    while error > tol and fx0 != 0 and dfx0 != 0 and contador < ite:
        x1 = x0 - (fx0/dfx0)
        fx0 = funcionF(x1)
        dfx0 = funcionFP(x1)
        error = math.fabs((x1 -x0)/x1)
        contador += 1
        x0 = x1
        print('{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(x0),str(fx0),str(dfx0),str(error)))

    if fx0 == 0:
        print(x0, "es raiz")
    else:
        if error < tol:
            print(x1, "se aproxima a una raiz con una tolerancia: ", tol)
        else:
            if dfx0 == 0:
                print(x1, "es una posible raiz multiple")
            else:
                print("Maximo de iteraciones alcanzadas")

def funcionF(entrada):
    global fx

    #fx = (x**2)-(6*x)+3
    #fx = (x**3) + 4*(x**2) - 10
    fx = exp((-x**2)+1) - 4*x**3 + 25
    return fx.subs(x,entrada)

def funcionFP(entrada):
    fpx = fx.diff(x)
    return fpx.subs(x, entrada)

def main():
    llamadasSistema()
    busquedas()

if __name__ == "__main__":
    main()