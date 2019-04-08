#!/usr/bin/python3

from sympy import * 
import sympy as sy
import numpy as np

x0 = 0.0
x1 = 0.0
delta = 0.0
ite = 0.0
fx0 = 0.0
fx1 = 0.0
contador = 0
#lista = []

x = Symbol('x')

def llamadasSistema():
    global x0, delta, ite
    x0 = float(input('Introduce un X0: '))
    delta = float(input('Introduce un Delta: '))
    ite = int(input('Introduce un Número de Iteraciones: '))

def busquedas():
    global x0, contador
    fx0 = funcion(x0)

    print('{:30},{:30},{:30}'.format('n','x0','f(x0)'))
    if fx0 == 0:
        print(x0, " es raiz")
    else:
        #lista.append([contador, x0, fx0])
        x1 = x0 + delta
        fx1 = funcion(x1)
        contador = 1
        print('{:30},{:30},{:30}'.format(str(0),str(x0),str(fx0)))
        while (fx0 * fx1) > 0 and contador <= ite:
            #fx1 = fx0
            x0 = x1
            fx0 = fx1
            #lista.append([contador, x0, fx0])
            x1 = x1 + delta
            fx1 = funcion(x1)
            print('{:30},{:30},{:30}'.format(str(contador),str(x0),str(fx0)))
            contador += 1

        print('{:30},{:30},{:30}'.format(str(contador),str(x1),str(fx1)))    
        #lista.append([contador,x1,fx1])
        if fx1 == 0:
            print(x1 + " es raiz")
        elif (fx0 * fx1) < 0:
            print("Hay una raiz entre ", x0, " y ", x1)
            #print(lista)
        else : 
            print ("Numero de iteraciones alcanzadas")

def funcion(entrada):
    #fx = (x**2)-(6*x)+3
    #fx = (x**3) + 4*(x**2) - 9.47
    #fx = cos((2 * x)-1) + 4 * sin(x - 3)
    #fx = x**3 + 4*(x**2) - 10
    #fx = ln((x**2)+3)-(6*x)*cos((14*x)-10)
    #fx = cos((7*x)-8)*exp((-x**2)+4) + ln((x**4)+3) - x - 15
    fx = exp((-x**2)+3) - 5*x**2
    return fx.subs(x,entrada)

def main():
    llamadasSistema()
    busquedas()

if __name__ == "__main__":
    main()