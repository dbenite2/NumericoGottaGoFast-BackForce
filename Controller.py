#!/usr/bin/python3

from sympy import *
import sympy as sy
import numpy as np
import math


x0 = 0.0
x1 = 0.0
delta = 0.0
ite = 0
fx0 = 0
fx1 = 0
fx  = 0
fpx = 0
fp2x = 0
fg = 0
xinf = 0
xsup = 0
tol = 0
contador = 0
x = Symbol('x')

'''Class for switching cases''' 
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        #Return the match method once, then stop
        yield self.match
        raise StopIteration("There's more than 10 numbers in the file")

    def match(self, *args):
        #Indicate whether or not to enter a case suite
        if self.fall or not args:
            return True
        elif self.value in args: 
            self.fall = True
            return True
        else:
            return False




def seleccion():
    global fx
    fx = input('Ingrese la función: ')
    intervalo = str(input("Desea hallar intervalos?: "))
    if(intervalo == "si" or intervalo == "Si" or intervalo == "yes" or intervalo ==  "Yes"):
        llamadasSistemaC()
        busquedas()
    while True:
        metodo = input('Seleccione el método: [1] biseccion, [2] regla_falsa, [3] punto_fijo, [4] newton, [5] secante, [6] raices_multiples: ')
        switcher(int(metodo))
        if metodo is None:
            print("Programa finalizado")
            break

def switcher(metodo):
    global fg
    for case in switch(metodo):

        if case(1):
            llamadasSistemaM()
            biseccion()
            break
        if case(2):
            llamadasSistemaM()
            reglaFalsa()
            break
        if case(3):
            fg = input('Ingrese la funcion Fg: ')
            llamadasSistemaT()
            puntoFijo()
            break
        if case(4):
            llamadasSistemaT()
            newton()
            break
        if case(5):
            llamadasSistemaS()
            secante()
            break
        if case(6):
            llamadasSistemaT
            rmultiple()
            break

def funcion(entrada):
    global fx
    x = entrada
    return eval(fx)

def funcionG(entrada):
    global fg
    x = entrada
    return eval(fg)

def funcionP(entrada):
    global fx,fpx
    fpx = fx.diff(entrada)
    x = entrada
    return eval(fpx)

def funcionP2(entrada):
    global fpx,fp2x
    fp2x = fpx.diff(entrada)
    x = entrada
    return eval(fp2x)

def llamadasSistemaC():
    global x0, delta, ite
    x0 = float(input('Introduce un X0: '))
    delta = float(input('Introduce un Delta: '))
    ite = int(input('Introduce un Número de Iteraciones: '))

def llamadasSistemaM():
    global xinf, xsup, ite, tol
    xinf = float(input('Introduce un Xinferior: '))
    xsup = float(input('Introduce un xsuperior: '))
    tol = float(input('Introduce una tolerancia: '))
    ite = int(input('Introduce un Número de Iteraciones: '))

def llamadasSistemaT():
    global x0, ite, tol
    x0 = float(input('Introduce un X0: '))
    tol = float(input('Introduce una tolerancia: '))
    ite = int(input('Introduce un Número de Iteraciones: ')) 

def llamadasSistemaS():
    global x0, x1, ite, tol
    x0 = float(input('Introduce un X0: '))
    x1 = float(input('Introduce un x1: '))
    tol = float(input('Introduce una tolerancia: '))
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


def biseccion():
    global xinf, xsup, tol, ite

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

def reglaFalsa():
    global xinf, xsup, tol, ite
    print('{:30},{:30},{:30},{:30},{:30},{:30}'.format('Iter','Xi','Xs','Xm','f(Xm)','Error'))

    fxinf = funcion(xinf)
    fxsup = funcion(xsup)

    if fxinf == 0:
        print(xinf, " es raiz")
    else:
        if fxsup == 0:
            print(xsup, " es raiz")
        elif (fxinf * fxsup) < 0:
            xm = xinf - ((fxinf * (xsup - xinf) / (fxsup - fxinf)))
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
                xm = xinf - ((fxinf * (xsup - xinf) / (fxsup - fxinf)))
                fxm = funcion(xm)
                error = math.fabs(xm - temp)
                print('{:30},{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(xinf),str(xsup),str(xm),str(fxm),str(error)))
                contador += 1
            print('{:30},{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(xinf),str(xsup),str(xm),str(fxm),str(error)))
            
            if fxm == 0:
                print(xm, " es raiz")
            else:
                if error < tol:
                    print(xm, " es una aproximación a una raiz con tolerancia: ",tol)
                else:
                    print("Número de iteraciones alcanzadas")
        else:
            print("El intervalo es inadecuado")

def puntoFijo():
    global x0, tol, ite

    fx = funcion(x0)
    contador = 0
    error = tol + 1
    print('{:30},{:30},{:30},{:30}'.format('n','xn','fxn','error'))
    while fx != 0 and error > tol and contador < ite:
        xn = funcionG(x0) 
        fx = funcion(xn)
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

def newton():
    global x0, tol, ite

    fx0 = funcion(x0)
    dfx0 = funcionP(x0)
    error = tol + 1
    contador = 0
    print('{:30},{:30},{:30},{:30},{:30}'.format('n','xn','f(xn)','d(xn)','error'))

    while error > tol and fx0 != 0 and dfx0 != 0 and contador < ite:
        x1 = x0 - (fx0/dfx0)
        fx0 = funcion(x1)
        dfx0 = funcionP(x1)
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

def secante():
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

def rmultiple():
    
    global x0, tol, ite

    fx0 = funcion(x0)
    dfx0 = funcionP(x0)
    d2fx0 = funcionP2(x0)
    den = (dfx0**2) - (fx0*d2fx0)
    error = tol + 1
    contador = 0
    print('{:30} {:30} {:30} {:30} {:30} {:30}'.format('Iterations', 'x', 'fx', 'dfx', 'd2f', 'error'))

    while (fx0 != 0) and (error > tol) and (den != 0)  and (contador < ite):
        den = (dfx0**2) - (fx0*d2fx0)
        x1 = x0 - ((fx0 * dfx0) / den)
        fx0 = funcion(x1)
        dfx0 = funcionP(x1)
        d2fx0 = funcionP2(x1)
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


def main():
    seleccion()

if __name__ == "__main__":
    main()