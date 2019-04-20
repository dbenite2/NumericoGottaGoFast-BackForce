#!/usr/bin/python3

from sympy import * 
import sympy as sy
import numpy as np
import math

x0 = 0
tol = 0
ite = 0
fx = 0
fpx = 0
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
    d2fx0 = funcionFP2(x0)
    den = (dfx0**2) - (fx0*d2fx0)
    error = tol + 1
    contador = 0
    print('{:30} {:30} {:30} {:30} {:30} {:30}'.format('Iterations', 'x', 'fx', 'dfx', 'd2f', 'error'))

    while (fx0 != 0) and (error > tol) and (den != 0)  and (contador < ite):
        den = (dfx0**2) - (fx0*d2fx0)
        x1 = x0 - ((fx0 * dfx0) / den)
        fx0 = funcionF(x1)
        dfx0 = funcionFP(x1)
        d2fx0 = funcionFP2(x1)
        error = math.fabs((x1 -x0)/x1)
        contador += 1
        x0 = x1
        print('{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(x0),str(fx0),str(dfx0),str(d2fx0),str(error)))

    if fx0 == 0:
        print(x0, "es raiz")
    else:
        if error < tol:
            print(x1, "se aproxima a una raiz con una tolerancia: ", tol)
        else:
            if dfx0 == 0:
                print(x1, "es una posible raiz multiple")
            elif d2fx0 == 0:
                print(x1, "es una posible raiz multiple")
            else:
                print("Maximo de iteraciones alcanzadas")

def funcionF(entrada):
    global fx

    #fx = (x**2)-(6*x)+3
    #fx = (x**3) + 4*(x**2) - 10
    #fx = exp((-x**2)+1) - 4*x**3 + 25
    fx = (x**4) - 18*(x**2) + 81
    return fx.subs(x,entrada)

def funcionFP(entrada):
    global fpx
    fpx = fx.diff(x)
    #print("primera derivada: ",fpx)
    return fpx.subs(x, entrada)

def funcionFP2(entrada): 
    fp2x = fpx.diff(x)
    #print("Segunda derivada: ",fp2x)
    return fp2x.subs(x,entrada)

def main():
    llamadasSistema()
    busquedas()

if __name__ == "__main__":
    main()