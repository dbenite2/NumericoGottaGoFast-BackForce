#!/usr/bin/python3

from sympy import * 
import sympy as sy
import numpy as np
import math

x0 = 0
tol = 0
ite = 0
error_type = 1

x = Symbol('x')

def llamadasSistema():
    global x0, ite, tol, error_type
    x0 = float(input('Introduce un X0: '))
    tol = float(input('Introduce una tolerancia: '))
    ite = int(input('Introduce un Número de Iteraciones: '))
    #error_type = int(input("ingrese el tipo de error [1] = absoluto; [0] = relativo: "))

def busquedas():
    global x0, tol, ite

    fx = funcionF(x0)
    contador = 0
    error = tol + 1
    print('{:30},{:30},{:30},{:30}'.format('n','xn','fxn','error'))
    while fx != 0 and error > tol and contador < ite:
        xn = funcionG(x0) 
        fx = funcionF(xn)
        error =  math.fabs(xn-x0)
        x0 = xn 
        print('{:30},{:30},{:30},{:30}'.format(str(contador),str(xn),str(fx),str(error)))
        contador += 1
    #print('{:30},{:30},{:30},{:30}'.format(str(contador),str(xn),str(fx),str(error)))
    if fx == 0:
        print(x0, " es raiz")
    else:
        if error < tol:
            print(x0, " es aproximación con una tolerancia: ", tol)
            
            #print(error_type)
        else:
            print("El metodo fracaso por las iteraciones")

def funcionF(entrada):
    #fx = (x**2)-(6*x)+3
    #fx = (x**3) + 4*(x**2) - 10 
    fx = exp((-x**2)+3) - 5*x**2
    return fx.subs(x,entrada)

def funcionG(entrada):
    #gx = (x**2)-(6*x)+3
    #gx = x - (((x**3)+4*(x**2)-10)/(3*(x**2) + 8*x))
    gx = (exp((-x**2)+3)*(2*(x**2)+1) + 5*x**2)/((2*x)*(exp((-x**2)+3)+5))
    return gx.subs(x,entrada)

def main():
    llamadasSistema()
    busquedas()

if __name__ == "__main__":
    main()