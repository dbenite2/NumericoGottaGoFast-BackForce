#!/usr/bin/python3

from sympy import * 
import sympy as sy
import numpy as np
import math

x0 = 0
x1 = 0
tol = 0
ite = 0
lista = []

x = Symbol('x')

def llamadasSistema():
    global x0, x1, ite, tol
    x0 = float(input('Introduce un X0: '))
    x1 = float(input('Introduce un x1: '))
    tol = float(input('Introduce una tolerancia: '))
    ite = int(input('Introduce un Número de Iteraciones: '))

def busquedas():
    global x1, x0, tol, ite

    fx0 = funcion(x0) 

    print('{:30},{:30},{:30},{:30}'.format('n', 'xn', 'f(xn)', 'error'))
    if fx0 == 0:
        print(x0, " es raiz")
    else: 
        fx1 = funcion(x1)
        error = tol + 1
        contador = 0
        denominador = fx1 - fx0
        while fx1 != 0 and error > tol and denominador != 0 and contador < ite:
            x2 = x1 - ((fx1 * (x1 - x0)) / denominador)
            error = math.fabs((x2 - x1)/x2)
            x0 = x1
            fx0 = fx1
            x1 = x2
            fx1 = funcion(x1)
            denominador = fx1 - fx0
            print('{:30},{:30},{:30},{:30}'.format(str(contador),str(x1),str(fx1),str(error)))
            contador += 1
        print('{:30},{:30},{:30},{:30}'.format(str(contador),str(x1),str(fx1),str(error)))
        if fx1 == 0:
            print(x1, " es una raiz")
        else:
            if error < tol:
                print(x1, " se aproxima a una raiz con una tolerancia: ", tol)
            else:
                if denominador == 0:
                    print(x1, " es una posible rai multiple")
                else: 
                    print("Maximo numero de iteraciones alcanzadas")

def funcion(entrada):
    #fx = (x**2)-(6*x)+3
    fx = cos((7*x)-8)*exp((-x**2)+4) + ln((x**4)+3) - x - 15
    return fx.subs(x,entrada)

def main():
    llamadasSistema()
    busquedas()

if __name__ == "__main__":
    main()