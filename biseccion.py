#!/usr/bin/python3

from sympy import * 
import sympy as sy
import numpy as np
import math

xinf = 0
xsup = 0
xm = 0
tol = 0
ite = 0
#lista = []

x = Symbol('x')

def llamadasSistema():
    global xinf, xsup, ite, tol
    xinf = float(input('Introduce un Xinferior: '))
    xsup = float(input('Introduce un xsuperior: '))
    tol = float(input('Introduce una tolerancia: '))
    ite = int(input('Introduce un Número de Iteraciones: '))

def busquedas():
    global xinf, xsup, xm, tol, ite

    print('{:30},{:30},{:30},{:30},{:30},{:30}'.format('Iter','Xi','Xs','Xm','f(Xm)','Error'))
    fxinf = funcion(xinf)
    fxsup = funcion(xsup)

    if fxinf == 0:
        print(xinf, " es raiz")
    elif fxsup == 0:
        print(xsup, " es raiz")
    elif (fxinf * fxsup) < 0:
        xm = (xinf + xsup) / 2
        fxm = funcion(xm)
        contador = 1
        error = tol + 1
        print('{:30},{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(xinf),str(xsup),str(xm),str(fxm),str(error)))

        while fxm != 0 and error > tol and contador < ite:
            if (fxinf * fxm) < 0:
                xsup = xm
                fxsup = fxm
            else:
                xinf = xm
                fxinf = fxm
            temp = xm 
            xm = (xinf + xsup) / 2
            fxm = funcion(xm)
            error = math.fabs(xm - temp)
            print('{:30},{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(xinf),str(xsup),str(xm),str(fxm),str(error)))
            contador += 1

        print('{:30},{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(xinf),str(xsup),str(xm),str(fxm),str(error)))
        if fxm == 0:
            print(xm, " es raiz")
        elif error < tol:
            print("En la iteración:" , contador)
            print(xm, " es una aproximación a una raiz con tolerancia: ",tol)
            print("El error fue de: ", error)
        else:
            print("Número de iteraciones alcanzadas")
    else:
            print("El intervalo es inadecuado")

def funcion(entrada):
    #fx = (x**2)-(6*x)+3
    #fx = exp((-x**2)+1) - 4*(x**3) + 25
    #fx = x**3 + 4*(x**2) - 10
    fx = ln((x**2)+3)-(6*x)*cos((14*x)-10)
    return fx.subs(x,entrada)

def main():
    llamadasSistema()
    busquedas()

if __name__ == "__main__":
    main()