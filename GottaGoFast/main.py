#Ejecución principal del programa Gotta Go Fast
#en este se reciben las peticiones del cliente web y se redirige al método correspondiente
#Desarrollado por: Jose Miguel Alzate. David Alejandro Benitez. Juan Pablo Londoño. Jennifer Maria Palacio

from __future__ import division
from flask import Flask, request, render_template,redirect,url_for
from flask_caching import Cache
from sympy import * 
from fractions import Fraction
import matplotlib.pyplot as plt
import pylab
import sympy as sy
import numpy as np
import math
from sympy import *
from sympy.parsing.sympy_parser import parse_expr,convert_xor,standard_transformations,implicit_multiplication,implicit_application,function_exponentiation,factorial_notation,rationalize
import os
from math import pi

#Sets iniciales para los manejos de funciones, expresiones y errores.
np.seterr(all = 'raise',divide = 'raise', invalid = 'raise')
f = Function('fx')
X = Symbol('x')
transformations = standard_transformations + (convert_xor,implicit_multiplication,implicit_application)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def paginaPrincipal():
    return render_template("inicio.html")

#-------------------------------------------------ECUACIONES DE UNA VARIABLE-------------------------------------------------

@app.route('/busquedasIncrementales')
def busquedas_incrementales():
    return render_template("busquedasIncrementales.html")

@app.route('/biseccion')
def biseccion():
    return render_template("biseccion.html")

@app.route('/reglaFalsa')
def reglaFalsa():
    return render_template("reglaFalsa.html")
 
@app.route('/puntoFijo')
def punto_fijo():
    return render_template("puntoFijo.html")

@app.route('/newton') 
def newton():
    return render_template("newton.html")

@app.route('/raicesMultiples')
def raices_multiples():
    return render_template("raicesMultiples.html")
 

@app.route('/secante')
def secante():
    return render_template("secante.html")

#Ejecución inicial del método para busquedas incrementales
@app.route('/busquedasIncrementales', methods=['GET','POST'])
def Busquedas_incrementales():
    global f
    x = Symbol('x')
    metodo = request.form.get('selector1')
    if (metodo == "0") or (metodo == "busquedasIncrementales"):
        #recolección de datos desde el cliente web con controles de entrada
        ejecuciones = []
        f = parse_expr(request.form.get('fx'),transformations=transformations)
        x0 = float(request.form.get('x0'))
        puntoInicial = x0
        delta = float(request.form.get('delta'))
        if delta == 0:
            return render_template('busquedasIncrementales.html', error = 1, mensajeError = 'El numero de pasos debe ser un numero diferente a 0', fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
        ite = int(request.form.get('ite'))
        if ite < 0:
            return render_template('busquedasIncrementales.html', error = 1, mensajeError = 'El numero de iteraciones debe ser mayor a 0',fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
        try:
            fx0 = Funcion_f(f,x0)
        except (ValueError, TypeError, NameError):
            return render_template('busquedasIncrementales.html', error = 1, mensajeError = 'Hay un error en la expresión ingresada',fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
        #fx0 = Funcion_f(f,x0)
        if fx0 == 0:
            graficar(0,f,'',puntoInicial,'',delta/10)
            return render_template('busquedasIncrementales.html', grafica = 1 ,x1 = x0, raiz = 1, error = 0, fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
        else:
            #Procesamiento de los datos según la funcionalidad del método
            x1 = x0 + delta
            fx1 = Funcion_f(f,x1)
            contador = 1
            ejecuciones.append([0,str(x0),str("{:+.2e}".format(fx0))])
            while fx0*fx1 > 0 and contador < ite:
                fx0 = fx1
                x0 = x1
                x1 = x1 + delta
                fx1 = Funcion_f(f,x1)
                ejecuciones.append([contador,str(x0),str("{:+.2e}".format(fx0))])
                contador += 1
            if fx1 == 0:
                fx0 = fx1
                x0n = x1
                ejecuciones.append([contador,str(x0n),str(fx0)])
                graficar(1,f,'',puntoInicial,x0n,delta/10)
                return render_template('busquedasIncrementales.html',grafica = 1, x1 = x1, raiz = 2, error = 0,ejecuciones = ejecuciones, n = contador , fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
            elif (fx0 * fx1) < 0:
                fx0 = fx1
                x0n = x1
                graficar(1,f,'',puntoInicial,x0n,delta/10)
                ejecuciones.append([contador,x0n,fx0])
                return render_template('busquedasIncrementales.html',grafica = 1, n = contador, ejecuciones = ejecuciones , raiz = 3, error = 0, x0 = x0, x1 = x1,fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
            else: 
                fx0 = fx1
                x0n = x1
                graficar(1,f,'',puntoInicial,x0n, delta/10)
                ejecuciones.append([contador,str(x0n),str(fx0)])
                return render_template('busquedasIncrementales.html',grafica = 1, n = contador, ejecuciones = ejecuciones , raiz = 0, error = 0, x0 = x0, x1 = x1, fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
    else:
        if (metodo == "biseccion") or (metodo == "reglaFalsa") or (metodo == "secante"):
            f = parse_expr(request.form.get('fx'))
            #x0 = float(request.form.get('x0'))
            #ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f)
        elif (metodo == "puntoFijo") or (metodo == "newton") or (metodo == "raicesMultiples"):
            f = parse_expr(request.form.get('fx'))
            #x0 = float(request.form.get('x0'))
            #ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f)

#Ejecución inicial del método para Bisección
@app.route('/biseccion', methods=['GET','POST'])
def Biseccion():
    global f
    metodo = request.form.get('selector1')
    e = int(request.form.get('selector2'))
    if (metodo == "0") or (metodo == "biseccion"):
        x = Symbol('x')
        ejecuciones = []
        #Recolección de los datos desde el cliente web con controles de entrada
        try:
            f = parse_expr(request.form.get('fx'),transformations=transformations)
        except (ValueError, TypeError, NameError):
            return render_template('biseccion.html', error = 1, mensajeError = 'Hay un error en la expresión ingresada',fx = request.form.get('fx'), x0i = request.form.get('x0'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        xi = float(request.form.get('xinf'))
        puntoInicial = xi
        xs = float(request.form.get('xsup'))
        puntoFinal = xs
        if xi == xs:
            return render_template('biseccion.html', error = 1, tol = request.form.get('tol'), mensajeError = 'El intervalo es invalido', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        tol = float(request.form.get('tol'))
        if tol == 0:
            return render_template('biseccion.html', error = 1, tol = request.form.get('tol'), mensajeError = 'La tolerancia debe ser diferente de 0', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        ite = int(request.form.get('ite'))
        if ite <= 0:
            return render_template('biseccion.html', error = 1, tol = request.form.get('tol'), mensajeError = 'El numero de iteraciones debe ser mayor a 0', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        try:
            fxi = Funcion_f(f,xi)
            fxs = Funcion_f(f,xs)
        except (ValueError, TypeError, NameError):
            return render_template('biseccion.html', error = 1, mensajeError = 'Hay un error en la expresión ingresada',fx = request.form.get('fx'), x0i = request.form.get('x0'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        graficar(1,f,'',puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
        if fxi == 0:
            return render_template('biseccion.html', grafica = 1 , error = 0, raiz = 1, xm = xi, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs == 0:
            return render_template('biseccion.html',grafica = 1 , error = 0, raiz = 1, xm = xs, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs*fxi > 0:
            return render_template('biseccion.html', grafica = 1 , error = 1, mensajeError = 'En el intervalor ingresado no hay ninguna raiz', tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        else:
            #Procesamiento de los datos según la funcionalidad del método
            xm = (xi + xs) / 2
            fxm = Funcion_f(f,xm)
            ejecuciones.append([0,str(xm),str("{:+.2e}".format(fxm)),'No Hay','No Hay'])
            contador = 1
            error = tol + 1
            while fxm != 0 and error > tol and contador < ite:
                if fxi * fxm < 0:
                    xs = xm
                    fxs = Funcion_f(f,xs)
                else:
                    xi = xm
                    fxi = Funcion_f(f,xi)
                xmAnt = xm
                xm = (xi + xs) / 2
                fxm = Funcion_f(f,xm)
                if e == 0:
                    error = abs(xm - xmAnt)
                elif e == 1:
                    if(xm != 0):
                        error = abs((xm - xmAnt)/xm)
                    else:
                        error = 0
                ejecuciones.append([contador,xm,"{:+.2e}".format(fxm),"{:.2e}".format(error)])
                contador = contador + 1
            if fxm == 0:
                return render_template('biseccion.html', e = e, grafica = 1 ,raiz = 2, xm = xm, ejecuciones = ejecuciones, tolFinal = "{:.2e}".format(error) , n = contador ,tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            elif error < tol:
                return render_template('biseccion.html',e = e, grafica = 1 , raiz = 3, xm = xm, ejecuciones = ejecuciones, tolFinal = "{:.2e}".format(error) , n = contador ,tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            else:
                return render_template('biseccion.html',e = e, grafica = 1 , raiz = 0, xm = xm, ejecuciones = ejecuciones, tolFinal = "{:.2e}".format(error) , n = contador ,tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
    else:
        if (metodo == "reglaFalsa") or (metodo == "secante"):
            f = parse_expr(request.form.get('fx'))
            # xi = float(request.form.get('xinf'))
            # xs = float(request.form.get('xsup'))
            # tol = float(request.form.get('tol'))
            # ite = int(request.form.get('ite'))
            # return render_template(metodo + ".html", fx = f, xinf = xi, xsup = xs, tol = tol, ite = ite)
            return render_template(metodo + ".html", fx = f)
        elif (metodo == "puntoFijo") or (metodo == "newton") or (metodo == "raicesMultiples") or (metodo == "busquedasIncrementales"):
            f = parse_expr(request.form.get('fx'))
            # xi = float(request.form.get('xinf'))
            # tol = float(request.form.get('tol'))
            # ite = int(request.form.get('ite'))
            # return render_template(metodo + ".html", fx = f, x0 = xi, tol = tol, ite = ite, x0i = xi)
            return render_template(metodo + ".html", fx = f)

#Ejecución inicial del método para Regla falsa
@app.route('/reglaFalsa', methods=['GET','POST'])
def Regla_falsa():
    global f
    metodo = request.form.get('selector1')
    e = int(request.form.get('selector2'))
    if (metodo == "0")  or (metodo == "reglaFalsa"):
        x = Symbol('x')
        ejecuciones = []
        #Recolección de datos desde el cliente web con controles de entrada
        f = parse_expr(request.form.get('fx'),transformations=transformations)
        xi = float(request.form.get('xinf'))
        xs = float(request.form.get('xsup'))
        if xi == xs:
            return render_template('reglaFalsa.html', error = 1, tol = request.form.get('tol'), mensajeError = 'El intervalo es invalido', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        tol = float(request.form.get('tol'))
        if tol == 0:
            return render_template('reglaFalsa.html', error = 1, tol = request.form.get('tol'), mensajeError = 'La tolerancia debe ser diferente de 0', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        ite = int(request.form.get('ite'))
        if ite <= 0:
            return render_template('reglaFalsa.html', error = 1, tol = request.form.get('tol'), mensajeError = 'El numero de iteraciones debe ser mayor a 0', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        try:
            fxi = Funcion_f(f,xi)
            fxs = Funcion_f(f,xs)
        except:
            return render_template('reglaFalsa.html', error = 1, tol = request.form.get('tol'), mensajeError = 'Hay un error en la expresión ingresada', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        puntoInicial = xi
        puntoFinal = xs
        graficar(1,f,'',puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
        if fxi == 0:
            return render_template('reglaFalsa.html', grafica = 1, error = 0, raiz = 1, xm = xi, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs == 0:
            return render_template('reglaFalsa.html', grafica = 1,  error = 0, raiz = 1, xm = xs, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs*fxi > 0:
            return render_template('reglaFalsa.html', grafica = 1, error = 1, mensajeError = 'En el intervalor ingresado no hay ninguna raiz', tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        else:
            #Procesamiento de los datos según la funcionalidad del método
            xm = xi - (fxi*(xs-xi))/(fxs-fxi)
            fxm = Funcion_f(f,xm)
            ejecuciones.append([0, xm, "{:+.2e}".format(fxm), 'No Hay', 'No Hay'])
            contador = 1
            error = tol + 1
            while fxm != 0 and error > tol and contador < ite:
                if fxi * fxm < 0:
                    xs = xm
                    fxs = Funcion_f(f,xs)
                else:
                    xi = xm
                    fxi = Funcion_f(f,xi)
                xmAnt = xm
                xm = xi - (fxi*(xs-xi))/(fxs-fxi)
                fxm = Funcion_f(f,xm)
                if e == 0:
                    error = abs(xm - xmAnt)
                elif e == 1:
                    if(xm != 0):
                        error = abs((xm - xmAnt)/xm)
                    else:
                        error = 0
                ejecuciones.append([contador, xm, "{:+.2e}".format(fxm), "{:.2e}".format(error)])
                contador = contador + 1
            if fxm == 0:
                return render_template('reglaFalsa.html',e = e, grafica = 1, raiz = 2, xm = xm, ejecuciones = ejecuciones, tolFinal = "{:.2e}".format(error) , n = contador ,tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            elif error < tol:
                return render_template('reglaFalsa.html',e = e, grafica = 1, raiz = 3, xm = xm, ejecuciones = ejecuciones, tolFinal = "{:.2e}".format(error) , n = contador ,tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            else:
                return render_template('reglaFalsa.html',e = e, grafica = 1, raiz = 0, xm = xm, ejecuciones = ejecuciones, tolFinal = "{:.2e}".format(error) , n = contador ,tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
    else:
        if (metodo == "biseccion") or (metodo == "secante"):
            f = parse_expr(request.form.get('fx'))
            # xi = float(request.form.get('xinf'))
            # xs = float(request.form.get('xsup'))
            # tol = float(request.form.get('tol'))
            # ite = int(request.form.get('ite'))
            # return render_template(metodo + ".html", fx = f, xinf = xi, xsup = xs, tol = tol, ite = ite)
            return render_template(metodo + ".html", fx = f)
        elif (metodo == "puntoFijo") or (metodo == "newton") or (metodo == "raicesMultiples") or (metodo == "busquedasIncrementales"):
            f = parse_expr(request.form.get('fx'))
            # xi = float(request.form.get('xinf'))
            # tol = float(request.form.get('tol'))
            # ite = int(request.form.get('ite'))
            # return render_template(metodo + ".html", fx = f, x0 = xi, tol = tol, ite = ite, x0i = xi)
            return render_template(metodo + ".html", fx = f)

#Ejecución inicial del método para Punto fijo
@app.route('/puntoFijo',methods = ['GET','POST'])
def Punto_fijo():
    global f 
    metodo = request.form.get('selector1')
    e = int(request.form.get('selector2'))
    if(metodo == "0" or metodo == "puntoFijo"):
        ejecuciones = []
        #Recolección de datos desde el cliente web con controles de entrada
        try:
            f = parse_expr(request.form.get('fx'),transformations=transformations)
        except (ValueError, TypeError, NameError):
            return render_template('puntoFijo.html', error = 1, tol = request.form.get('tol'), mensajeError = 'Hay un error en la expresión ingresada ', fx = request.form.get('fx'), gx = request.form.get('gx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        g = parse_expr(request.form.get('gx'),transformations=transformations)
        x0 = float(request.form.get('x0'))
        tol = float(request.form.get('tol'))
        ite = int(request.form.get('ite'))
        if tol == 0:
            return render_template('puntoFijo.html', error = 1, tol = request.form.get('tol'), mensajeError = 'La tolerancia debe ser diferente de 0', fx = request.form.get('fx'), gx = request.form.get('gx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        ite = int(request.form.get('ite'))
        if ite <= 0: 
            return render_template('puntoFijo.html', error = 1, tol = request.form.get('tol'), mensajeError = 'El número de iteraciones debe ser mayor a 0', fx = request.form.get('fx'), gx = request.form.get('gx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        puntoInicial = x0
        primerPunto = x0
        try:
            fxa = Funcion_f(f,x0)
        except (ValueError, TypeError, NameError):
            return render_template('puntoFijo.html', error = 1, tol = request.form.get('tol'), mensajeError = 'Hay un error en la expresión fx ingresada ', fx = request.form.get('fx'), gx = request.form.get('gx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        try:
            controlGx = Funcion_f(g,x0)
        except (ValueError, TypeError, NameError):
            return render_template('puntoFijo.html', error = 1, tol = request.form.get('tol'), mensajeError = 'Hay un error en la expresión gx ingresada ', fx = request.form.get('fx'), gx = request.form.get('gx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        #Procesamiento de los datos según la funcionalidad del método            
        contador = 0
        error = tol + 1
        ejecuciones.append([contador, x0, "{:+.2e}".format(fxa),'No Hay'])
        while fxa != 0 and error > tol and contador < ite:
            xn = Funcion_f(g,x0)
            fxa = Funcion_f(f,x0)
            if e == 0:
                error = abs(xn - x0)
            elif e == 1:
                if(xn != 0):
                    error = abs((xn - x0)/xn)
                else:
                    error = 0
            x0 = xn
            if(contador == 0):
                primerPunto = x0
            contador += 1
            ejecuciones.append([contador,x0,"{:+.2e}".format(fxa),"{:.2e}".format(error)])
        if(abs(abs(puntoInicial)-abs(primerPunto)) > abs(abs(puntoInicial)-abs(x0))):
            puntoFinal = primerPunto
        else:
            puntoFinal = x0
        if(puntoInicial == puntoFinal):
                puntoInicial = puntoInicial-2
                puntoFinal = puntoFinal+2
        if fxa == 0:
            graficar(2,f,g,puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
            return render_template('puntoFijo.html',e = e, grafica = 1, raiz = 2, xs = x0, ejecuciones = ejecuciones, tolFinal ="{:.2e}".format(error), tol = request.form.get('tol'), n = contador, fx = request.form.get('fx'), gx = request.form.get('gx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        elif error < tol:
            graficar(2,f,g,puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
            return render_template('puntoFijo.html',e = e, grafica = 1, raiz = 3, xs = x0, ejecuciones = ejecuciones, tolFinal = "{:.2e}".format(error), tol = request.form.get('tol'), n = contador, fx = request.form.get('fx'), gx = request.form.get('gx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        else:
            graficar(2,f,g,puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
            return render_template('puntoFijo.html',e = e, grafica = 1, raiz = 0, xs = x0, ejecuciones = ejecuciones, tolFinal = "{:.2e}".format(error), tol = request.form.get('tol'), n = contador, fx = request.form.get('fx'), gx = request.form.get('gx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
    else:
        if (metodo == "reglaFalsa") or (metodo == "secante") or (metodo == "biseccion"):
            f = parse_expr(request.form.get('fx'))
            # xi = float(request.form.get('xinf'))
            # xs = float(request.form.get('xsup'))
            # tol = float(request.form.get('tol'))
            # ite = int(request.form.get('ite'))
            # return render_template(metodo + ".html", fx = f, xinf = xi, xsup = xs, tol = tol, ite = ite)
            return render_template(metodo + ".html", fx = f)
        elif (metodo == "newton")  or (metodo == "raicesMultiples") or (metodo == "busquedasIncrementales"):
            f = parse_expr(request.form.get('fx'))
            # xi = float(request.form.get('xinf'))
            # tol = float(request.form.get('tol'))
            # ite = int(request.form.get('ite'))
            # return render_template(metodo + ".html", fx = f, x0 = xi, tol = tol, ite = ite, x0i = xi)
            return render_template(metodo + ".html", fx = f)

#Ejecución inicial del método para Newton
@app.route('/newton', methods = ['GET','POST'])
def Newton():
    global f
    metodo = request.form.get('selector1')
    e = int(request.form.get('selector2'))
    if(metodo == "0" or metodo == "newton"):
        ejecuciones = []
        #Recolección de los datos con control de datos
        try:
            f = parse_expr(request.form.get('fx'),transformations=transformations)
        except:
            return render_template('newton.html', error = 1, tol = request.form.get('tol'), mensajeError = 'Hay un error en la expresión ingresada', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        x0 = float(request.form.get('x0'))
        tol = float(request.form.get('tol'))
        if tol == 0:
            return render_template('newton.html', error = 1, tol = request.form.get('tol'), mensajeError = 'La tolerancia debe ser diferente de 0', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        ite = int(request.form.get('ite'))
        if ite <= 0: 
            return render_template('newton.html', error = 1, tol = request.form.get('tol'), mensajeError = 'El número de iteraciones debe ser mayor a 0', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        puntoInicial = x0
        primerPunto = x0
        try:
            fx0 = Funcion_f(f,x0)
            dfx0 = Funcion_p(f,x0)
        except: 
            return render_template('newton.html', error = 1, tol = request.form.get('tol'), mensajeError = 'Hay un error en la expresión fx ingresada', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        #Procesamiento de los datos según la funcionalidad del método    
        error = tol + 1
        contador = 0
        ejecuciones.append([contador, x0, "{:+.2e}".format(fx0), 'No Hay', 'No Hay'])
        while fx0 != 0 and dfx0 != 0 and error > tol and contador < ite:
            x1 = x0 - (fx0/dfx0)
            fx0 = Funcion_f(f,x1)
            dfx0 = Funcion_p(f,x1)
            if e == 0:
                error = abs(x1 - x0)
            elif e == 1:
                if(x1 != 0):
                    error = abs((x1 - x0)/x1)
                else:
                    error = 0
            x0 = x1
            if(contador == 0):
                primerPunto = x0
            contador += 1 
            ejecuciones.append([contador, x0, "{:+.2e}".format(fx0), "{:.2e}".format(error)])
        if(abs(abs(puntoInicial)-abs(primerPunto)) > abs(abs(puntoInicial)-abs(x0))):
            puntoFinal = primerPunto
        else:
            puntoFinal = x0
        if(puntoInicial == puntoFinal):
                puntoInicial = puntoInicial-2
                puntoFinal = puntoFinal+2
        if fx0 == 0:
            graficar(1,f,'',puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
            return render_template('newton.html',e = e, grafica = 1, raiz = 2, xs = x0, ejecuciones = ejecuciones, n = contador, tolFinal = "{:.2e}".format(error), tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        elif error < tol:
            graficar(1,f,'',puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
            return render_template('newton.html',e = e, grafica = 1, raiz = 3, xs = x0, ejecuciones = ejecuciones, n = contador, tolFinal = "{:.2e}".format(error),  tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        elif dfx0 == 0:
            graficar(1,f,'',puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
            return render_template('newton.html',e = e, grafica = 1, raiz = 4, xs = x0, ejecuciones = ejecuciones, n = contador, tolFinal = "{:.2e}".format(error),  tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        else:
            graficar(1,f,'',puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
            return render_template('newton.html',e = e, grafica = 1, raiz = 0, xs = x0, ejecuciones = ejecuciones, n = contador, tolFinal = "{:.2e}".format(error),  tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
    else:
        if (metodo == "reglaFalsa") or (metodo == "secante") or (metodo == "biseccion"):
            f = parse_expr(request.form.get('fx'))
            #xi = float(request.form.get('xinf'))
            #xs = float(request.form.get('xsup'))
            #tol = float(request.form.get('tol'))
            #ite = int(request.form.get('ite'))
            #return render_template(metodo + ".html", fx = f, xinf = xi, xsup = xs, tol = tol, ite = ite)
            return render_template(metodo + ".html", fx = f)
        elif (metodo == "puntoFijo")  or (metodo == "raicesMultiples") or (metodo == "busquedasIncrementales"):
            f = parse_expr(request.form.get('fx'))
            #xi = float(request.form.get('xinf'))
            #tol = float(request.form.get('tol'))
            #ite = int(request.form.get('ite'))
            #return render_template(metodo + ".html", fx = f, x0 = xi, tol = tol, ite = ite, x0i = xi)
            return render_template(metodo + ".html", fx = f)

#Ejecución inicial del método para Secante
@app.route('/secante', methods=['GET','POST'])
def Secante():
    global f
    metodo = request.form.get('selector1')
    e = int(request.form.get('selector2'))
    if (metodo == "0")  or (metodo == "secante"):
        # x = Symbol('x')
        ejecuciones = []
        #Recolección de los datos desde el cliente web con control de entrada
        try:
            f = parse_expr(request.form.get('fx'),transformations=transformations)
        except:
            return render_template('secante.html', error = 1, tol = request.form.get('tol'), mensajeError = 'Hay un error en la expresión ingresada', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        xi = float(request.form.get('xinf'))
        xs = float(request.form.get('xsup'))
        if xi == xs:
            return render_template('secante.html', error = 1, tol = request.form.get('tol'), mensajeError = 'El intervalo es invalido', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        tol = float(request.form.get('tol'))
        if tol == 0:
            return render_template('secante.html', error = 1, tol = request.form.get('tol'), mensajeError = 'La tolerancia debe ser diferente de 0', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        ite = int(request.form.get('ite'))
        if ite <= 0:
            return render_template('secante.html', error = 1, tol = request.form.get('tol'), mensajeError = 'El número de iteraciones debe ser mayor a 0', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        try:
            fxi = Funcion_f(f,xi)
            fxs = Funcion_f(f,xs)
        except:
            return render_template('secante.html', error = 1, tol = request.form.get('tol'), mensajeError = 'Hay un error en la expresión fx ingresada', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        puntoInicial = xi
        puntoFinal = xs
        graficar(1,f,'',puntoInicial,puntoFinal,abs((puntoInicial-puntoFinal)/100))
        if fxi == 0:
            return render_template('secante.html', grafica = 1, error = 0, raiz = 1, xm = xi, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs == 0:
            return render_template('secante.html', grafica = 1, error = 0, raiz = 1, xm = xs, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs*fxi > 0:
            return render_template('secante.html', error = 1, mensajeError = 'En el intervalor ingresado no hay ninguna raiz', tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        else:
            #Procesamiento de los datos según la funcionalidad del método
            contador = 0
            error = tol + 1
            denominador = fxs - fxi
            ejecuciones.append([contador, xs, "{:+.2e}".format(fxs), 'No Hay'])
            while fxs != 0 and error > tol and denominador != 0 and contador < ite:
                xn = (xs - (fxs*(xs-xi)/denominador))
                if e == 0:
                    error = abs(xn - xs)
                elif e == 1:
                    if(xn != 0):
                        error = abs((xn - xs)/xn)
                    else:
                        error = 0
                xi = xs
                fxi = fxs
                xs = xn
                fxs = Funcion_f(f,xs)
                denominador = fxs - fxi     
                contador += 1
                ejecuciones.append([contador, xs, "{:+.2e}".format(fxs), "{:.2e}".format(error)])
            if fxs == 0:
                return render_template('secante.html',e = e, grafica = 1, raiz = 2, xm = xs, ejecuciones = ejecuciones, tolFinal = "{:.2e}".format(error), tol = request.form.get('tol'), n = contador, fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            elif error < tol:
                return render_template('secante.html',e = e, grafica = 1, raiz = 3, xm = xs, ejecuciones = ejecuciones, tolFinal = "{:.2e}".format(error),  tol = request.form.get('tol'), n = contador, fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            elif denominador == 0 :
                return render_template('secante.html',e = e, grafica = 1, raiz = 4, xm = xs, ejecuciones = ejecuciones, tolFinal = "{:.2e}".format(error), tol = request.form.get('tol'), n = contador, fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            else:
                return render_template('secante.html',e = e, grafica = 1, raiz = 0, xm = xs, ejecuciones = ejecuciones, tolFinal = "{:.2e}".format(error), tol = request.form.get('tol'), n = contador, fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
    else:
        if (metodo == "biseccion") or (metodo == "reglaFalsa"):
            f = parse_expr(request.form.get('fx'))
            # xi = float(request.form.get('xinf'))
            # xs = float(request.form.get('xsup'))
            # tol = float(request.form.get('tol'))
            # ite = int(request.form.get('ite'))
            # return render_template(metodo + ".html", fx = f, xinf = xi, xsup = xs, tol = tol, ite = ite)
            return render_template(metodo + ".html", fx = f)
        elif (metodo == "puntoFijo") or (metodo == "newton") or (metodo == "raicesMultiples") or (metodo == "busquedasIncrementales"):
            f = parse_expr(request.form.get('fx'))
            # xi = float(request.form.get('xinf'))
            # tol = float(request.form.get('tol'))
            # ite = int(request.form.get('ite'))
            # return render_template(metodo + ".html", fx = f, x0 = xi, tol = tol, ite = ite, x0i = xi)
            return render_template(metodo + ".html", fx = f)

#Ejecución inicial del método para Raices Multiples
@app.route('/raicesMultiples', methods = ['GET','POST'])
def Raices_multiples():
    global f
    metodo = request.form.get('selector1')
    e = int(request.form.get('selector2'))
    if (metodo == "0") or (metodo == "raicesMultiples"):
        ejecuciones = []
        try:
            f = parse_expr(request.form.get('fx'),transformations=transformations)
        except:
            return render_template('raicesMultples.html', error = 1, tol = request.form.get('tol'), mensajeError = 'Hay un error en la expresión ingresada', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        x0 = float(request.form.get('x0'))
        tol = float(request.form.get('tol'))
        if tol == 0:
            return render_template('raicesMultples.html', error = 1, tol = request.form.get('tol'), mensajeError = 'La toleraciona debe de ser diferente de 0', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        ite = int(request.form.get('ite'))
        if ite <= 0:
            return render_template('raicesMultples.html', error = 1, tol = request.form.get('tol'), mensajeError = 'El número de iteraciones debe de ser mayor a 0', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        puntoInicial = x0
        primerPunto = x0
        try:
            fx0 = Funcion_f(f,x0)
            dfx0 = Funcion_p(f,x0)
            d2fx0 = Funcion_p2(f,x0)
        except:
            return render_template('raicesMultples.html', error = 1, tol = request.form.get('tol'), mensajeError = 'Hay un error en la expresión ingresada', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        den = (dfx0**2) - (fx0*d2fx0)
        error = tol + 1 
        contador = 0
        ejecuciones.append([contador, x0, "{:+.2e}".format(fx0), "{:+.2e}".format(dfx0), 'No Hay', 'No Hay'])
        while (fx0 != 0) and (error > tol) and (den != 0) and (contador < ite):
            den = (dfx0*dfx0) - (fx0*d2fx0)
            x1 = x0 - ((fx0 * dfx0) / den)
            fx0 = float(Funcion_f(f,x1))
            dfx0 = float(Funcion_p(f,x1))
            d2fx0 = float(Funcion_p2(f,x1))
            if e == 0:
                error = abs(x1 - x0)
            elif e == 1:
                if(x1 != 0):    
                    error = abs((x1 - x0)/x1)
                else:
                    error = 0
            x0 = x1
            if(contador == 0):
                primerPunto = x0
            contador += 1
            ejecuciones.append([contador, x0, "{:+.2e}".format(fx0), "{:+.2e}".format(dfx0) , "{:.2e}".format(error)])
        if(abs(abs(puntoInicial)-abs(primerPunto)) > abs(abs(puntoInicial)-abs(x0))):
            puntoFinal = primerPunto
        else:
            puntoFinal = x0
        if(puntoInicial == puntoFinal):
                puntoInicial = puntoInicial-2
                puntoFinal = puntoFinal+2
        if fx0 == 0:
            graficar(1,f,'',puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
            return render_template('raicesMultiples.html',e = e, grafica = 1, raiz = 2, xs = x0, ejecuciones = ejecuciones, n = contador, tolFinal = "{:.2e}".format(error), tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        elif error < tol:
            graficar(1,f,'',puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
            return render_template('raicesMultiples.html',e = e, grafica = 1, raiz = 3, xs = x0, ejecuciones = ejecuciones, n = contador, tolFinal = "{:.2e}".format(error), tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        elif dfx0 == 0:
            graficar(1,f,'',puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
            return render_template('raicesMultiples.html',e = e, grafica = 1, raiz = 4, xs = x0, ejecuciones = ejecuciones, n = contador, tolFinal = "{:.2e}".format(error), tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        else:
            graficar(1,f,'',puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
            return render_template('raicesMultiples.html',e = e, grafica = 1, raiz = 0, xs = x0, ejecuciones = ejecuciones, n = contador, tolFinal = "{:.2e}".format(error), tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
    else:
        if (metodo == "reglaFalsa") or (metodo == "secante") or (metodo == "biseccion"):
            f = parse_expr(request.form.get('fx'))
            # xi = float(request.form.get('xinf'))
            # xs = float(request.form.get('xsup'))
            # tol = float(request.form.get('tol'))
            # ite = int(request.form.get('ite'))
            # return render_template(metodo + ".html", fx = f, xinf = xi, xsup = xs, tol = tol, ite = ite)
            return render_template(metodo + ".html", fx = f)
        elif (metodo == "puntoFijo")  or (metodo == "newton") or (metodo == "busquedasIncrementales"):
            f = parse_expr(request.form.get('fx'))
            # xi = float(request.form.get('xinf'))
            # tol = float(request.form.get('tol'))
            # ite = int(request.form.get('ite'))
            # return render_template(metodo + ".html", fx = f, x0 = xi, tol = tol, ite = ite, x0i = xi)
            return render_template(metodo + ".html", fx = f)

#-------------------------------------------------ECUACIONES DE UNA VARIABLE-------------------------------------------------




#-------------------------------------------------- SISTEMAS DE ECUACIONES---------------------------------------------------
#Se inicia con las vistas iniciales antes de cualquier ejecución 
@app.route('/eliminacionGaussiana')
def eliminacionGaussiana():
    return render_template("eliminacionGaussiana.html")

@app.route('/pivoteoTotal')
def pivoteoTotal():
    return render_template("pivoteoTotal.html")

@app.route('/pivoteoParcial')
def pivoteoParcial():
    return render_template("pivoteoParcial.html")

@app.route('/pivoteoEscalonado')
def pivoteoEscalonado():
    return render_template("pivoteoEscalonado.html")

@app.route('/crout')
def crout():
    return render_template("crout.html")
    
@app.route('/doolittle')
def doolittle():
    return render_template("doolittle.html")

@app.route('/cholesky')
def cholesky():
    return render_template("cholesky.html")

@app.route('/jacobi')
def jacobi():
    return render_template("jacobi.html")

@app.route('/gaussSeidel')
def gaussSeidel():
    return render_template("gaussSeidel.html")

#Generacion de las matrices visuales según el método seleccionado 
@app.route('/eliminacionGaussianaM', methods = ['GET','POST'])
def EliminacionGaussianaM():
    n = int(request.form.get('n'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    return render_template("eliminacionGaussiana.html", dibujarMatrizInicial = 1, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

@app.route('/pivoteoTotalM', methods = ['GET','POST'])
def PivoteoTotalM():
    n = int(request.form.get('n'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    return render_template("pivoteoTotal.html", dibujarMatrizInicial = 1, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

@app.route('/pivoteoParcialM', methods = ['GET','POST'])
def PivoteoParcialM():
    n = int(request.form.get('n'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    return render_template("pivoteoParcial.html", dibujarMatrizInicial = 1, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

@app.route('/pivoteoEscalonadoM', methods = ['GET','POST'])
def PivoteoEscalonadoM():
    n = int(request.form.get('n'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    return render_template("pivoteoEscalonado.html", dibujarMatrizInicial = 1, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

@app.route('/croutM', methods = ['GET','POST'])
def CroutM():
    n = int(request.form.get('n'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    return render_template("crout.html", dibujarMatrizInicial = 1, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

@app.route('/doolittleM', methods = ['GET','POST'])
def DoolittleM():
    n = int(request.form.get('n'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    return render_template("doolittle.html", dibujarMatrizInicial = 1, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

@app.route('/choleskyM', methods = ['GET','POST'])
def CholeskyM():
    n = int(request.form.get('n'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    return render_template("cholesky.html", dibujarMatrizInicial = 1, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

@app.route('/jacobiM', methods = ['GET','POST'])
def JacobiM():
    n = int(request.form.get('n'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    iniciales = ['' for i in range(n)]
    return render_template("jacobi.html", dibujarMatrizInicial = 1, matrizInicial = matrizInicial, iniciales = iniciales, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

@app.route('/gaussSeidelM', methods = ['GET','POST'])
def GaussSeidelM():
    n = int(request.form.get('n'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    iniciales = ['' for i in range(n)]
    return render_template("gaussSeidel.html", dibujarMatrizInicial = 1, matrizInicial = matrizInicial, iniciales = iniciales, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

#Metodos operacionales
#Ejecución inicial del método para Eliminación Gaussiana
@app.route('/eliminacionGaussiana', methods = ['GET','POST'])
def EliminacionGaussiana():
    np.seterr(divide = 'raise', invalid = 'raise') #Control de errores por parte de Numpy
    verProcedimiento = int(request.form.get('selector'))
    cambiarMetodo = str(request.form.get('selector1'))
    #Recolección de datos por parte del cliente web con control de errores
    tam = int(request.form.get('n'))
    indiceColumnas = [i for i in range(tam+1)]
    indiceFilas= [i for i in range(tam)]
    matrizInicial = [['' for i in range(tam+1)] for j in range(tam)]
    matrizSolucion = [['' for i in range(tam+1)] for j in range(tam)]
    procedimiento = []
    for i in range(tam):
        for j in range(tam+1):
            indice = str(i)+str(j)
            try:
                matrizInicial[i][j] = float(Fraction(request.form.get(indice)))
            except(ValueError, TypeError, NameError):
                return render_template("eliminacionGaussiana.html", error = 1, mensajeError = "Por favor ingresa únicamente números", dibujarMatrizInicial = 1,matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = tam)
    casicero = 0
    if cambiarMetodo == '0':   
        # Gauss elimxina hacia adelante
        AB = np.vstack(matrizInicial)
        tamano = np.shape(AB)
        n = tamano[0]
        m = tamano[1]
        for i in range(0,n,1):
            pivote = AB[i,i]
            adelante = i+1 
            for k in range(adelante,n,1):
                if (np.abs(AB[k,i])>=casicero):
                    try:
                        coeficiente = pivote/AB[k,i]
                    except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                        matrizSolucion = np.vstack(AB)
                        return render_template("eliminacionGaussiana.html", error = 1, mensajeError = "Se produjo una division por cero. Abortando.",verProcedimiento = verProcedimiento ,procedimiento = procedimiento, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizInicial = matrizInicial, matrizSolucion = matrizSolucion, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = tam)
                    coeficiente = pivote/AB[k,i]                        
                    AB[k,:] = AB[k,:]*coeficiente - AB[i,:]
                else:
                    coeficiente= 'division para cero'
                procedimiento.append(np.vstack(AB))
        matrizSolucion = np.vstack(AB)
        # Gauss-Jordan elimina hacia atras
        ultfila = n-1
        ultcolumna = m-1
        for i in range(ultfila,0-1,-1):
            # Normaliza a 1 elemento diagonal
            try:
                AB[i,:] = AB[i,:] / AB[i,i]
            except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                X = AB[:,ultcolumna]
                X = np.transpose([X])
                return render_template("eliminacionGaussiana.html", error = 1, mensajeError = "Se produjo una division por cero. Abortando",verProcedimiento = verProcedimiento ,procedimiento = procedimiento, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizInicial = matrizInicial, matrizSolucion = matrizSolucion, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = tam, X = X)                
                
            pivote = AB[i,i] # uno
            # arriba de la fila i
            atras = i-1 
            for k in range(atras,0-1,-1):
                if (np.abs(AB[k,i])>=casicero):
                    try:
                        coeficiente = pivote/AB[k,i]
                    except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                        return render_template("eliminacionGaussiana.html", error = 1, mensajeError = "Se produjo una division por cero. Abortando",verProcedimiento = verProcedimiento ,procedimiento = procedimiento, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizInicial = matrizInicial, matrizSolucion = matrizSolucion, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = tam)
                    AB[k,:] = AB[k,:]*coeficiente - AB[i,:]
                else:
                    coeficiente= 'division para cero'
        X = AB[:,ultcolumna]
        X = np.transpose([X])
        # SALIDA
        return render_template("eliminacionGaussiana.html",verProcedimiento = verProcedimiento ,procedimiento = procedimiento, X = X, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizInicial = matrizInicial, matrizSolucion = matrizSolucion, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = tam)
    else:
        return render_template(cambiarMetodo+".html", dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = tam)
#Ejecución inicial del método para Eliminación Gaussiana con Pivoteo Total
@app.route('/pivoteoTotal', methods = ['GET','POST'])
def PivoteoTotal():
    np.seterr(divide = 'raise', invalid = 'raise')#Control de errores por parte de Numpy
    verProcedimiento = int(request.form.get('selector'))
    cambiarMetodo = str(request.form.get('selector1'))
    #Recolección de datos desde el cliente web con control de errores
    n = int(request.form.get('n'))
    tam = n
    indiceColumnas = [i for i in range(tam+1)]
    indiceFilas= [i for i in range(tam)]
    matrizInicial = [['' for i in range(tam+1)] for j in range(tam)]
    matrizSolucion = [['' for i in range(tam+1)] for j in range(tam)]
    procedimiento = []
    for i in range(tam):
        for j in range(tam+1):
            indice = str(i)+str(j)
            try:
                matrizInicial[i][j] = float(Fraction(request.form.get(indice)))
            except(ValueError, TypeError, NameError):
                return render_template("pivoteoTotal.html", error = 1, mensajeError = "Por favor ingresa únicamente números", dibujarMatrizInicial = 1,matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = tam)
    
    if cambiarMetodo == '0':
        matrizInicial1 = np.vstack(matrizInicial)
        procedimiento.append(np.vstack(matrizInicial1))
        matrizSolucion = np.vstack(matrizInicial1)
        for k in range(0,n-1):
            matrizSolucion = linear_solver(matrizSolucion,k,n)
            procedimiento.append(np.vstack(matrizSolucion))  
            for i in range(k+1,n):
                try:
                    mult = matrizSolucion[i][k] / matrizSolucion[k][k]
                except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                    return render_template("pivoteoTotal.html",verProcedimiento = verProcedimiento, error = 1, mensajeError = "Se produjo una division por cero. Abortando", procedimiento = procedimiento, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizInicial = matrizInicial, matrizSolucion = matrizSolucion, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
                for j in range(k,n+1):
                    matrizSolucion[i][j] = matrizSolucion[i][j] - mult * matrizSolucion[k][j]
            procedimiento.append(np.vstack(matrizSolucion))         
        x = [0 for i in range(n)]
        try:
            x[n-1] = float(matrizSolucion[n-1][n])/matrizSolucion[n-1][n-1]
        except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
            X = np.traspose([x])
            return render_template("pivoteoTotal.html", X = X, verProcedimiento = verProcedimiento, error = 1, mensajeError = "Se produjo una division por cero. Abortando", procedimiento = procedimiento, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizInicial = matrizInicial, matrizSolucion = matrizSolucion, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        for i in reversed(range(0,n)):
            z = 0
            for j in range(i+1,n):
                z = z + float(matrizSolucion[i][i]) * x[j]
            try:
                x[i] = float(matrizSolucion[i][n] - z) / matrizSolucion[i][i]
            except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                X = np.traspose([x])
                return render_template("pivoteoTotal.html", X = X, verProcedimiento = verProcedimiento, error = 1, mensajeError = "Se produjo una division por cero. Abortando", procedimiento = procedimiento, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizInicial = matrizInicial, matrizSolucion = matrizSolucion, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        X = np.transpose([x])
        return render_template("pivoteoTotal.html",verProcedimiento = verProcedimiento, X = X, procedimiento = procedimiento, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizInicial = matrizInicial, matrizSolucion = matrizSolucion, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    else:
        return render_template(cambiarMetodo+".html", dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
#Ejecución inicial del método para Eliminación Gaussiana con pivoteo parcial
@app.route('/pivoteoParcial', methods = ['GET','POST'])
def PivoteoParcial():
    np.seterr(divide = 'raise', invalid = 'raise')#Control de errores por parte de Numpy
    verProcedimiento = int(request.form.get('selector'))
    cambiarMetodo = str(request.form.get('selector1'))
    #Recolección de datos por parte del cliente web con control de entrada
    n = int(request.form.get('n'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    matrizSolucion = [['' for i in range(n+1)] for j in range(n)]
    procedimiento = []
    for i in range(n):
        for j in range(n+1):
            indice = str(i)+str(j)
            try:
                matrizInicial[i][j] = float(Fraction(request.form.get(indice)))
            except(ValueError, TypeError, NameError):
                return render_template("pivoteoParcial.html", error = 1, mensajeError = "Por favor ingresa únicamente números", dibujarMatrizInicial = 1,matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

    M = np.vstack(matrizInicial)
    if cambiarMetodo == '0':
        for k in range(n):
            print("iteracion ",k)
            for i in range(k,n):
                if abs(M[i][k]) > abs(M[k][k]):
                    M[k], M[i] = M[i],M[k]
                else:
                    pass
            for j in range(k+1,n):
                try:
                    q = float(M[j][k]) / M[k][k]
                except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                    return render_template("pivoteoParcial.html", error = 1,verProcedimiento = verProcedimiento, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizSolucion = M, matrizInicial = matrizInicial, mensajeError = "Se presentó una división por cero. Se aborta la ejecución")
                for m in range(k, n+1):
                    M[j][m] -=  q * M[k][m]
            #print de analisis
            print(M)
            procedimiento.append(M)
        X = [0 for i in range(n)]
        try:
            X[n-1] =float(M[n-1][n])/M[n-1][n-1]
        except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
            return render_template("pivoteoParcial.html", error = 1,verProcedimiento = verProcedimiento, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizSolucion = M, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, X = X, mensajeError = "Se presentó una división por cero. Se aborta la ejecución")
        for i in range (n-1,-1,-1):
            z = 0
            for j in range(i+1,n):
                z = z  + float(M[i][j])*X[j]
            try:
                X[i] = float(M[i][n] - z)/M[i][i]
            except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                return render_template("pivoteoParcial.html", error = 1,verProcedimiento = verProcedimiento, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizSolucion = M, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, X = X, mensajeError = "Se presentó una división por cero. Se aborta la ejecución")
        X = np.transpose([X])
        return render_template("pivoteoParcial.html",verProcedimiento = verProcedimiento, X = X, procedimiento = procedimiento, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizInicial = matrizInicial, matrizSolucion = M, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    else:
        return render_template(cambiarMetodo+".html", dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

@app.route('/pivoteoEscalonado', methods = ['GET','POST'])
def PivoteoEscalonado():
    np.seterr(divide = 'raise', invalid = 'raise')
    n = int(request.form.get('n'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    matrizSolucion = [['' for i in range(n+1)] for j in range(n)]
    for i in range(n):
        for j in range(n+1):
            indice = str(i)+str(j)
            try:
                matrizInicial[i][j] = float(Fraction(request.form.get(indice)))
            except(ValueError, TypeError, NameError):
                return render_template("pivoteoEscalonado.html", error = 1, mensajeError = "Por favor ingresa únicamente números", dibujarMatrizInicial = 1,matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    
    return render_template("pivoteoEscalonado.html", dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizInicial = matrizInicial, matrizSolucion = matrizSolucion, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

#Ejecución inicial del método para Crout
@app.route('/crout', methods = ['GET','POST'])
def Crout():
    np.seterr(divide = 'raise', invalid = 'raise')
    verProcedimiento = int(request.form.get('selector'))
    cambiarMetodo = str(request.form.get('selector1'))
    #Recolección de datos por parte del cliente web con control de entrada
    n = int(request.form.get('n'))
    procedimientoL = []
    procedimientoU = []
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matriz_i = [['' for i in range(n+1)] for j in range(n)]
    matriz_s = [['' for i in range(n+1)] for j in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    L = [[0.0 for j in range(n)] for i in range(n)]
    U = [[1.0 if j == i else 0.0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n+1):
            indice = str(i)+str(j)
            try:
                matrizInicial[i][j] = float(Fraction(request.form.get(indice)))
            except(ValueError, TypeError, NameError):
                return render_template("crout.html", error = 1, mensajeError = "Por favor ingresa únicamente números", dibujarMatrizInicial = 1,matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    if cambiarMetodo == '0':
        for i in range(n):
            for j in range(n+1):
                indice = str(i)+str(j)
                try:
                    matriz_i[i][j] = float(Fraction(request.form.get(indice)))
                    matriz_s[i][j] = float(Fraction(request.form.get(indice)))
                except(ValueError, TypeError, NameError):
                    return render_template("crout.html", error = 1, mensajeError = "Por favor ingresa únicamente números", dibujarMatrizInicial = 1,matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        matriz_i = np.vstack(matriz_i)
        matriz_s = np.vstack(matriz_s)
        b = matriz_s[0:n,n]
        matriz_s = np.delete(matriz_s,n,1)
        for k in range(0,n):
            suma_1 = 0.0
            for p in range(0,k):
                suma_1 += (L[k][p] * U[p][k])
            L[k][k] = (matriz_s[k][k] - suma_1)
            U[k][k] = 1
            for i in range(k+1,n):
                suma_2 = 0.0 
                for p in range(0,k):
                    suma_2 += (L[i][p] * U[p][k])
                if L[k][k] != 0:
                    try:
                        L[i][k] = (matriz_s[i][k] - suma_2) / U[k][k]
                        procedimientoL.append(np.vstack(L))
                    except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                        return render_template("crout.html",dibujarMatrizInicial = 1, error = 1, mensajeError = "Se produjo una división por 0. Abortando", matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
            for j in range(k+1,n):
                suma_3 = 0.0
                for p in range(0,k):
                    suma_3 += L[k][p] * U[p][j]
                if L[k][k] != 0:
                    try:
                        U[k][j] = (matriz_s[k][j] - suma_3) / L[k][k]
                        procedimientoU.append(np.vstack(U))
                    except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                       return render_template("crout.html",dibujarMatrizInicial = 1, error = 1, mensajeError = "Se produjo una división por 0. Abortando", matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        try:                
            z = progresiva(L,b)
        except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                        return render_template("crout.html",dibujarMatrizInicial = 1,dibujarMatrizSolucion = 1 , error = 1, mensajeError = "Hubo un problema en la sustitución progresiva", matrizInicial = matriz_i,L = L, U = U, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        try:
            x = regresiva(U,z)
            X = np.transpose([x])
        except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                        return render_template("crout.html",dibujarMatrizInicial = 1,dibujarMatrizSolucion = 1 , error = 1, mensajeError = "Hubo un problema en la sustitución regresiva", matrizInicial = matriz_i,L = L, U = U, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        return render_template("crout.html",verProcedimiento = verProcedimiento, X = X, procedimientoL = procedimientoL, procedimientoU = procedimientoU, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizInicial = matrizInicial, matrizSolucionL = L, matrizSolucionU = U, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    else:
        return render_template(cambiarMetodo+".html", dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

#Ejecución inicial del método para Doolittle
@app.route('/doolittle', methods = ['GET','POST'])
def Doolittle():
    np.seterr(divide = 'raise', invalid = 'raise')#Control de errores por parte de Numpy
    #Recolección de datos desde el cliente web con control de entrada
    n = int(request.form.get('n'))
    procedimientoL = []
    procedimientoU = []
    verProcedimiento = int(request.form.get('selector'))
    cambiarMetodo = str(request.form.get('selector1'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matriz_i = [['' for i in range(n+1)] for j in range(n)]
    matriz_s = [['' for i in range(n+1)] for j in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    L = [[1.0 if j == i else 0.0 for j in range(n)] for i in range(n)]
    U = [[0.0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n+1):
            indice = str(i)+str(j)
            try:
                matriz_i[i][j] = float(Fraction(request.form.get(indice)))
                matriz_s[i][j] = float(Fraction(request.form.get(indice)))
                matrizInicial[i][j] = float(Fraction(request.form.get(indice)))
            except(ValueError, TypeError, NameError):
                return render_template("doolittle.html", error = 1, mensajeError = "Por favor ingresa únicamente números", dibujarMatrizInicial = 1,matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    matriz_i = np.vstack(matriz_i)
    matriz_s = np.vstack(matriz_s)
    b = matriz_s[:,n]
    matriz_s = np.delete(matriz_s,n,1)
    if cambiarMetodo == '0':
        for k in range(0,n):
            suma_1 = 0.0
            for p in range(0,k):
                suma_1 += (L[k][p] * U[p][k])
            L[k][k] = 1
            U[k][k] = matriz_s[k][k] - suma_1
            for i in range(k+1,n):
                suma_2 = 0.0 
                for p in range(0,k):
                    suma_2 += (L[i][p] * U[p][k])
                if L[k][k] != 0:
                    try:
                        L[i][k] = (matriz_s[i][k] - suma_2) / U[k][k]
                        procedimientoL.append(np.vstack(L))
                    except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                        return render_template("doolittle.html",dibujarMatrizInicial = 1, error = 1, mensajeError = "Se produjo una división por 0 o el sistema puede no tener solucion. Abortando", matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
            for j in range(k+1,n):
                suma_3 = 0.0
                for p in range(0,k):
                    suma_3 += L[k][p] * U[p][j]
                if L[k][k] != 0:
                    try:
                        U[k][j] = (matriz_s[k][j] - suma_3) / L[k][k]
                        procedimientoU.append(np.vstack(U))
                    except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                        return render_template("doolittle.html",dibujarMatrizInicial = 1, error = 1, mensajeError = "Se produjo una división por 0 o el sistema puede no tener solucion. Abortando", matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        try:
            z = progresiva(L,b)
        except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
            return render_template("doolittle.html",dibujarMatrizInicial = 1,dibujarMatrizSolucion = 1 , error = 1, mensajeError = "Hubo un problema en la sustitución progresiva", matrizInicial = matriz_i,L = L, U = U, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        try:
            x = regresiva(U,z)
            X = np.transpose([x])
        except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
            return render_template("doolittle.html",dibujarMatrizInicial = 1,dibujarMatrizSolucion = 1 , error = 1, mensajeError = "Hubo un problema en la sustitución regresiva", matrizInicial = matriz_i,L = L, U = U, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        return render_template("doolittle.html",verProcedimiento = verProcedimiento, X = X, procedimientoL = procedimientoL, procedimientoU = procedimientoU, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizInicial = matrizInicial, matrizSolucionL = L, matrizSolucionU = U, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    else:
        return render_template(cambiarMetodo+".html", dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
#Ejecución inicial del método para Cholesky
@app.route('/cholesky', methods = ['GET','POST'])
def Cholesky():
    np.seterr(divide = 'raise', invalid = 'raise')#control de errores por parte de Numpy
    #Recolección de datos desde el cliente web con control de entrada
    n = int(request.form.get('n'))
    verProcedimiento = int(request.form.get('selector'))
    cambiarMetodo = str(request.form.get('selector1'))
    procedimientoL = []
    procedimientoU = []
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matriz_i = [['' for i in range(n+1)] for j in range(n)]
    matriz_s = [['' for i in range(n+1)] for j in range(n)]
    matrizInicial = [['' for i in range(n+1)] for j in range(n)]
    L = [[1.0 if j == i else 0.0 for j in range(n)] for i in range(n)]
    U = [[1.0 if j == i else 0.0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n+1):
            indice = str(i)+str(j)
            try:
                matriz_i[i][j] = float(Fraction(request.form.get(indice)))
                matriz_s[i][j] = float(Fraction(request.form.get(indice)))
                matrizInicial[i][j] = float(Fraction(request.form.get(indice)))
            except(ValueError, TypeError, NameError):
                return render_template("cholesky.html", error = 1, mensajeError = "Por favor ingresa únicamente números", dibujarMatrizInicial = 1,matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

    matriz_i = np.vstack(matriz_i)
    matriz_s = np.vstack(matriz_s)
    b = matriz_s[:,n]
    matriz_s = np.delete(matriz_s,n,1)
    if cambiarMetodo == '0':
        for k in range(0,n):
            suma_1 = 0.0
            for p in range(0,k):
                suma_1 += (L[k][p] * U[p][k])
            try:
                L[k][k] = sqrt(matriz_s[k][k] - suma_1)
                procedimientoL.append(np.vstack(L))
            except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                return render_template("cholesky.html",dibujarMatrizInicial = 1, error = 1, mensajeError = "La solucion del sistema no se encuentra en los reales", matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
            U[k][k] = L[k][k]
            procedimientoU.append(np.vstack(U))
            for i in range(k+1,n):
                suma_2 = 0.0 
                for p in range(0,k):
                    suma_2 += (L[i][p] * U[p][k])
                if L[k][k] != 0:
                    try:
                        L[i][k] = (matriz_s[i][k] - suma_2) / U[k][k]
                        procedimientoL.append(np.vstack(L))
                    except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                        return render_template("cholesky.html",dibujarMatrizInicial = 1, error = 1, mensajeError = "Se produjo una división por 0 o el sistema puede no tener solucion. Abortando", matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
            for j in range(k+1,n):
                suma_3 = 0.0
                for p in range(0,k):
                    suma_3 += L[k][p] * U[p][j]
                if L[k][k] != 0:
                    try:
                        U[k][j] = (matriz_s[k][j] - suma_3) / L[k][k]
                        procedimientoU.append(np.vstack(U))
                    except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                        return render_template("cholesky.html",dibujarMatrizInicial = 1, error = 1, mensajeError = "Se produjo una división por 0 o el sistema puede no tener solucion. Abortando", matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        try:                
            z = progresiva(L,b)
        except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                        return render_template("cholesky.html",dibujarMatrizInicial = 1,dibujarMatrizSolucion = 1 , error = 1, mensajeError = "Hubo un problema en la sustitución progresiva", matrizInicial = matriz_i,L = L, U = U, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        try:
            x = regresiva(U,z)
            X = np.transpose([x])
        except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                        return render_template("cholesky.html",dibujarMatrizInicial = 1,dibujarMatrizSolucion = 1 , error = 1, mensajeError = "Hubo un problema en la sustitución regresiva", matrizInicial = matriz_i,L = L, U = U, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        return render_template("cholesky.html",verProcedimiento = verProcedimiento, X = X, procedimientoL = procedimientoL, procedimientoU = procedimientoU, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1,matrizInicial = matrizInicial, matrizSolucionL = L, matrizSolucionU = U, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    else:
        return render_template(cambiarMetodo+".html", dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, matrizInicial = matrizInicial, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

@app.route('/jacobi', methods = ['GET','POST'])
def Jacobi():
    np.seterr(divide = 'raise', invalid = 'raise')
    n = int(request.form.get('n'))
    cambiarMetodo = str(request.form.get('selector1'))
    tol = float(request.form.get('tol'))
    niter = int(request.form.get('ite'))
    error = int(request.form.get('selector2'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matriz_i = [['' for i in range(n+1)] for j in range(n)]
    matriz_s = [['' for i in range(n+1)] for j in range(n)]
    iniciales = [0 for i in range(n)]
    if tol == 0:
        return render_template("jacobi.html", error = 1,tol = float(request.form.get('tol')), ite = niter, mensajeError = "La tolerancia debe ser diferente de 0", dibujarMatrizInicial = 1,matrizInicial = matriz_i,iniciales = iniciales, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    if niter <= 0:
        return render_template("jacobi.html", error = 1,tol = tol, ite = int(request.form.get('ite')), mensajeError = "El número de iteraciones debe ser mayor que 0", dibujarMatrizInicial = 1,matrizInicial = matriz_i,iniciales = iniciales, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    resultados = [['N',['X'+str(i) for i in range(n)],'ERROR']]
    for i in range(n):
        for j in range(n+1):
            indice = str(i)+str(j)
            try:
                matriz_i[i][j] = float(Fraction(request.form.get(indice)))
                matriz_s[i][j] = float(Fraction(request.form.get(indice)))
            except(ValueError, TypeError, NameError):
                return render_template("jacobi.html", error = 1,tol = tol, ite = niter, mensajeError = "Por favor ingresa únicamente números", dibujarMatrizInicial = 1,matrizInicial = matriz_i,iniciales = iniciales, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        try:
            iniciales[i] = float(Fraction(request.form.get('iniciales'+str(i))))
        except(ValueError, TypeError, NameError):
                return render_template("jacobi.html", error = 1,tol = tol, ite = niter, mensajeError = "Por favor ingresa únicamente números", dibujarMatrizInicial = 1,matrizInicial = matriz_i,iniciales = iniciales, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    iniciales1 = iniciales
    if cambiarMetodo == '0':
        cont = 0
        disp = tol + 1
        matriz_i = np.vstack(matriz_i)
        matriz_s = np.vstack(matriz_s)
        b = matriz_s[:,n]
        matriz_s = np.delete(matriz_s,n,1)
        x1 = [0 for i in range(n)]
        resultados.append([cont,iniciales,disp])
        while disp > tol and cont < niter:
            try:
                x1 = calcular_nuevo_jacobi(iniciales,n,b,matriz_s)
            except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                    return render_template("jacobi.html", tol = tol, ite = niter,dibujarMatrizInicial = 1, iniciales = iniciales1, error = 1,mensajeError = "Se produjo una division por cero", resultados = resultados, matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n =  n)
            if error == 0:
                try:
                    disp = abs((norma(x1) - norma(iniciales)) / norma(x1))
                except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                    return render_template("jacobi.html", tol = tol, ite = niter,dibujarMatrizInicial = 1, iniciales = iniciales1, error = 1,mensajeError = "Se produjo una division por cero", resultados = resultados, matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n =  n)
            elif error == 1:
                disp = abs(norma(x1) - norma(iniciales))
            iniciales = x1
            cont = cont + 1
            resultados.append([cont, iniciales,disp])
        print(resultados)
        if disp < tol:
            return render_template("jacobi.html",  tol = tol, ite = niter,dibujarMatrizInicial = 1,dibujarMatrizSolucion = 1, matrizInicial = matriz_i,resultados = resultados, iniciales = iniciales1 ,indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        else: 
            return render_template("jacobi.html", tol = tol, ite = niter, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1, error = 1,mensajeError = "Fracaso en las iteraciones dadas", resultados = resultados, iniciales = iniciales1,matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n =  n)
        return render_template("jacobi.html", tol = tol, ite = niter, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1, matrizInicial = matriz_i, resultados = resultados, iniciales = iniciales1, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    else:
        if cambiarMetodo == 'gaussSeidel':
            return render_template(cambiarMetodo+".html", tol = tol, ite = niter,dibujarMatrizInicial = 1, iniciales = iniciales1, dibujarMatrizSolucion = 0, matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        else:
            return render_template(cambiarMetodo+".html", dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, iniciales = iniciales1, matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

@app.route('/gaussSeidel', methods = ['GET','POST'])
def GaussSeidel():
    np.seterr(divide = 'raise', invalid = 'raise')
    n = int(request.form.get('n'))
    cambiarMetodo = str(request.form.get('selector1'))
    tol = float(request.form.get('tol'))
    niter = int(request.form.get('ite'))
    error = int(request.form.get('selector2'))
    indiceColumnas = [i for i in range(n+1)]
    indiceFilas= [i for i in range(n)]
    matriz_i = [['' for i in range(n+1)] for j in range(n)]
    matriz_s = [['' for i in range(n+1)] for j in range(n)]
    iniciales = [0 for i in range(n)]
    if tol == 0:
        return render_template("gaussSeidel.html", error = 1,tol = float(request.form.get('tol')), ite = niter, mensajeError = "La tolerancia debe ser diferente de 0", dibujarMatrizInicial = 1,matrizInicial = matriz_i,iniciales = iniciales, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    if niter <= 0:
        return render_template("gaussSeidel.html", error = 1,tol = tol, ite = int(request.form.get('ite')), mensajeError = "El número de iteraciones debe ser mayor que 0", dibujarMatrizInicial = 1,matrizInicial = matriz_i,iniciales = iniciales, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    resultados = []
    for i in range(n):
        for j in range(n+1):
            indice = str(i)+str(j)
            try:
                matriz_i[i][j] = float(Fraction(request.form.get(indice)))
                matriz_s[i][j] = float(Fraction(request.form.get(indice)))
            except(ValueError, TypeError, NameError):
                return render_template("gaussSeidel.html", error = 1, tol = tol, ite = niter ,mensajeError = "Por favor ingresa únicamente números", dibujarMatrizInicial = 1,matrizInicial = matriz_i, iniciales = iniciales, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        try:    
            iniciales[i] = float(request.form.get('iniciales'+str(i)))
        except(ValueError, TypeError, NameError):
                return render_template("gaussSeidel.html", error = 1, tol = tol, ite = niter ,mensajeError = "Por favor ingresa únicamente números", dibujarMatrizInicial = 1,matrizInicial = matriz_i, iniciales = iniciales, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    iniciales1 = iniciales
    if cambiarMetodo == '0':
        matriz_i = np.vstack(matriz_i)
        matriz_s = np.vstack(matriz_s)
        cont = 0
        disp = tol + 1
        b = matriz_s[:,n]
        matriz_s = np.delete(matriz_s,n,1)
        x1 = [0 for i in range(n)]
        resultados.append([cont,iniciales,disp])
        while disp > tol and cont < niter:
            try:
                x1 = calcular_nuevo_seidel(iniciales,n,b,matriz_s)
            except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                    return render_template("gaussSeidel.html", tol = tol, ite = niter,dibujarMatrizInicial = 1, iniciales = iniciales1, error = 1,mensajeError = "Se produjo una division por cero", resultados = resultados, matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n =  n)
            if error == 1:
                try:
                    disp = abs((norma(x1) - norma(iniciales)) / norma(x1))
                except(ValueError, TypeError, NameError,ZeroDivisionError,RuntimeError,FloatingPointError):
                    return render_template("gaussSeidel.html", tol = tol, ite = niter, iniciales = iniciales1,dibujarMatrizInicial = 1,dibujarMatrizSolucion = 1, error = 1,mensajeError = "Se produjo una division por cero", resultados = resultados, matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n =  n)
            elif error == 0:
                disp = abs(norma(x1) - norma(iniciales))
            iniciales = x1
            cont = cont + 1
            resultados.append([cont,iniciales,disp])
        if disp < tol:
            return render_template("gaussSeidel.html", tol = tol, ite = niter, iniciales = iniciales1, dibujarMatrizInicial = 1,dibujarMatrizSolucion = 1, matrizInicial = matriz_i,resultados = resultados, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        else: 
            return render_template("gaussSeidel.html",  tol = tol, ite = niter,iniciales = iniciales1,dibujarMatrizInicial = 1,dibujarMatrizSolucion = 1, error = 1,mensajeError = "Fracaso en las iteraciones dadas", resultados = resultados, matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n =  n)
        return render_template("gaussSeidel.html", tol = tol, ite = niter, iniciales = iniciales1, dibujarMatrizInicial = 1,dibujarMatrizSolucion = 1, matrizInicial = matriz_i, resultados = resultados, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
    else:   
        if cambiarMetodo == 'jacobi':
            return render_template(cambiarMetodo+".html", iniciales = iniciales1, tol = tol, ite = niter,dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)
        else:
            return render_template(cambiarMetodo+".html", iniciales = iniciales1, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, matrizInicial = matriz_i, indiceColumnas = indiceColumnas, indiceFilas = indiceFilas, n = n)

#-----------------------------------------------------INTERPOLACIONES---------------------------------------------------------
@app.route('/newtonInt')
def interpolacionNewton():
    return render_template("newtonInterpolacion.html")

@app.route('/lagrange')
def interpolacion_lagrange():
    return render_template("lagrange.html")

# @app.route('/neville')
# def interpolacion_neville():
#     return render_template("nevile.html")


@app.route('/newtonIntM', methods = ['GET' , 'POST'])
def interpolacion_newton_t():
    n = int(request.form.get('puntos'))
    indiceColumnas = [i for i in range(n)]
    x = ['' for i in range(n)]
    fx = ['' for i in range(n)]
    return render_template("newtonInterpolacion.html", dibujarMatrizInicial = 1, indiceColumnas = indiceColumnas,x = x, fx = fx, puntos = n)

@app.route('/lagrangeM', methods = ['GET' , 'POST'])
def interpolacion_lagrange_t():
    n = int(request.form.get('puntos'))
    indiceColumnas = [i for i in range(n)]
    x = ['' for i in range(n)]
    fx = ['' for i in range(n)]
    return render_template("lagrange.html", dibujarMatrizInicial = 1, indiceColumnas = indiceColumnas,x = x, fx = fx, puntos = n)

# @app.route('/nevilleM', methods = ['GET' , 'POST'])
# def interpolacion_lagrange_t():
#     n = int(request.form.get('puntos'))
#     indiceColumnas = [i for i in range(n)]
#     x = ['' for i in range(n)]
#     fx = ['' for i in range(n)]
#     return render_template("nevile.html", dibujarMatrizInicial = 1, indiceColumnas = indiceColumnas,x = x, fx = fx, puntos = n)

@app.route('/newtonInt', methods = ['GET','POST'])
def InterpolacionNewton():
    np.seterr(divide = 'raise', invalid = 'raise')
    n = int(request.form.get('puntos'))
    cambiarMetodo = str(request.form.get('selector1'))
    indiceColumnas = [i for i in range(n)]
    val = float(request.form.get('valor'))
    x = [0 for i in range(n)]
    y = [0 for i in range(n)]
    for i in range(n):
        x[i] = float(request.form.get('x'+str(i)))
        y[i] = float(request.form.get('fx'+str(i)))
    aux = [[0 for i in range(n)] for j in range(n)]
    prod = 1.0
    acum = ''
    res = 0.0
    if cambiarMetodo == '0':
        for i in range(n):
            aux[i][0] = y[i]
            for j in range(1,i + 1):
                try:
                    aux[i][j] = (aux[i][j-1] - aux[i-1][j-1])/(x[i] - x[i-j])
                except(ValueError,TypeError,ZeroDivisionError,RuntimeError,FloatingPointError):
                    return render_template("newtonInterpolacion.html",error = "1", mensajeError = "Se produjo una división por cero.Abortando",acum = acum, puntos = n, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, indiceColumnas = indiceColumnas,valor = val, x = x, fx = y)
            if(i > 0):
                prod *= val-x[i-1]
            res += aux[i][i] * prod
            acum += str(aux[i][i])+'*'+str(prod)+'+'
        temp = len(acum)
        acum = acum[:temp - 1]
        print(aux)
        return render_template("newtonInterpolacion.html",acum = acum,res = res, puntos = n, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1, indiceColumnas = indiceColumnas, valor = val, x = x, fx = y)
    else:
        return render_template(cambiarMetodo+".html", puntos = n, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, indiceColumnas = indiceColumnas, valor = val, x = x, fx = y)


@app.route('/lagrange', methods = ['GET','POST'])
def lagrange():
    np.seterr(divide = 'raise', invalid = 'raise')
    n = int(request.form.get('puntos'))
    indiceColumnas = [i for i in range(n)]
    cambiarMetodo = str(request.form.get('selector1'))
    val = float(request.form.get('valor'))
    x = [0 for i in range(n)]
    y = [0 for i in range(n)]
    for i in range(n):
        x[i] = float(request.form.get('x'+str(i)))
        y[i] = float(request.form.get('fx'+str(i)))
    l = [0.0 for i in range(n)]
    acum = ''
    res = 0.0
    #valorfx = 0
    if cambiarMetodo == '0':
        for i in range(n):
            prod = 1.0
            for j in range(n):
                if(j != i):
                    try:
                        prod *= (val - x[j]) / (x[i] - x[j])
                    except(ValueError,TypeError,ZeroDivisionError,RuntimeError,FloatingPointError):
                        return render_template("newtonInterpolacion.html",error = "1", mensajeError = "Se produjo una división por cero.Abortando", puntos = n, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, indiceColumnas = indiceColumnas,valor = val, x = x, fx = y)
            l[i] = prod
            res += (l[i]*y[i])
            acum += str(l[i])+'*f(x'+str(i)+')+'
        temp = len(acum)
        acum = acum[:temp - 1]
        return render_template("lagrange.html",acum = acum,res = res, puntos = n, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1, indiceColumnas = indiceColumnas, valor = val, x = x, fx = y, )
    else:
        return render_template(cambiarMetodo+".html", puntos = n, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, indiceColumnas = indiceColumnas, valor = val, x = x, fx = y)

# @app.route('/neville', methods = ['GET','POST'])
# def neville():
#     n = int(request.form.get('puntos'))
#     indiceColumnas = [i for i in range(n)]
#     cambiarMetodo = str(request.form.get('selector1'))
#     val = float(request.form.get('valor'))
#     x = [0 for i in range(n)]
#     y = [0 for i in range(n)]
#     for i in range(n):
#         x[i] = float(request.form.get('x'+str(i)))
#         y[i] = float(request.form.get('fx'+str(i)))
#     valores = [[0 for i in range(n)] for j in range(n)]
#     acum = ''
#     res = 0.0
#     #valorfx = 0
#     if cambiarMetodo == '0':
#         for i in range(n):
#             valores[i][0] = y[i]
#         for i in range(n):
#             for j in range(1,i):
#                 try:
#                     valores[i][j] = ((val - x[i - j]) * valores[i][j-1] - ((val - x[i]) * valores[i - 1][j - 1])) / (x[i] - [i - j]) 

#         res = valores[n-1][n-1]
        
#         temp = len(acum)
#         acum = acum[:temp - 1]
        
#         return render_template("neville.html",acum = acum,res = res, puntos = n, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 1, indiceColumnas = indiceColumnas, valor = val, x = x, fx = y, )
#     else:
#         return render_template(cambiarMetodo+".html", puntos = n, dibujarMatrizInicial = 1, dibujarMatrizSolucion = 0, indiceColumnas = indiceColumnas, valor = val, x = x, fx = y)

#------------------------------------------------------------------------------------------------------------------

def linear_solver(A,k,n):
    mayor = 0
    fila_mayor = k
    columna_mayor = k
    marcas = [0 for i in range(n)]
    for i in range(1,n+1):
        marcas[i-1] = i
    for i in range(k,n):
        for j in range(k,n):
            if(abs(A[i][j]) > mayor):
                mayor = abs(A[i][j])
                fila_mayor = i
                columna_mayor = j
            else: 
                pass
    if mayor == 0:
        return None
    else:
        if fila_mayor != k:
            A = swap_rows(A,fila_mayor,k)
        if columna_mayor != k:
            A = swap_cols(A,columna_mayor,k)
            temp = marcas[columna_mayor]
            marcas[columna_mayor] = marcas[k]
            marcas[k] = temp
    return A

def swap_rows(A,row_A,row_B):
    A[row_A], A[row_B] = A[row_B], A[row_A]
    return A

def swap_cols(A,col_A,col_B):
    for i in range(len(A)):
        A[i][col_A], A[i][col_B] = A[i][col_B], A[i][col_A]
    return A

def progresiva(L,b):
    z = [0 for i in range(len(b))]
    z[0] = b[0] / L[0][0]
    for i in range(1,len(b)):
        sum = 0.0
        for j in range(0,i):
            sum += L[i][j] * z[j]
        z[i] = ((b[i] - sum)/L[i][i])
    return z

def regresiva(U,z):
    n = len(z)
    x = [0 for i in range(n)]
    x[n-1] = z[n-1]/U[n-1][n-1]
    for i in reversed((range(0,n-1))):
        sum = 0.0
        for j in range(i+1,n):
            sum += U[i][j] * x[j]
        x[i] = ((z[i] - sum)/U[i][i])
    return x

def calcular_nuevo_jacobi(x0, n, b, A):
    x1 = [0 for i in range(n)]
    for i in range(0,n):
        suma = 0.0
        for j in range(n):
            if j != i:
                suma += A[i][j] * x0[j]
            x1[i] = (b[i] - suma) / A[i][i]
    return x1

def calcular_nuevo_seidel(x0, n, b, A):
    x1 = [0 for i in range(n)]
    for i in range(0,n):
        x1[i] = x0[i]
    for i in range(0,n):
        suma = 0.0
        for j in range(0,n):
            if j != i:
                suma += A[i][j] * x1[j]
        x1 = (b[i] - suma) / A[i][i]
    return x1

def norma(x0):
    cont = 0
    for i in range(len(x0)):
        cont += abs(x0[i]) * abs(x0[i])
    return math.sqrt(cont)

def Funcion_f(fx,entrada):
    x = entrada
    fx = str(fx)
    print("fx: ",fx)
    print("eval: ", eval(fx))
    fx = eval(fx)
    fx = complex(fx)
    fx = fx.real
    return fx

def Funcion_p(fx,entrada):
    fpx = str(diff(fx,X))
    x = entrada
    print("f'x: ",fpx)
    print("eval: ", eval(fpx))
    fpx = eval(fpx)
    fpx = complex(fpx)
    fpx = fpx.real
    return fpx

def Funcion_p2(fx,entrada):
    fp2x = str(diff(fx,X,2))
    x = entrada
    print("f''x: ",fp2x)
    print("eval: ", eval(fp2x))
    fp2x = eval(fp2x)
    fp2x = complex(fp2x)
    fp2x = fp2x.real
    return fp2x

def graficar(opcion, funcion, funcion2, puntoInicial,puntoFinal, paso):
    global f
    x = Symbol('x')
    if(puntoInicial > puntoFinal):
        ac = puntoInicial
        puntoInicial = puntoFinal
        puntoFinal = ac
    if(opcion == 0):
        a=np.arange(puntoInicial-2,puntoInicial+2,paso)
        b=[Funcion_f(f,a[ai]) for ai in range(len(a))]
        plt.plot(a,b,label='f(x)')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Funcion f(x)')
        plt.autoscale()
        plt.grid()
        plt.legend(loc=1)
        plt.savefig('GottaGoFast\static\images\img.png')
        plt.delaxes()
    elif(opcion == 1):
        print('VALORES')
        a=np.arange(puntoInicial,puntoFinal,paso)
        b=[Funcion_f(f,a[ai]) for ai in range(len(a))]
        plt.plot(a,b,label='f(x)')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Funcion f(x)')
        plt.autoscale()
        plt.grid()
        plt.legend(loc=1)
        plt.savefig('GottaGoFast\static\images\img.png')
        plt.delaxes()
    elif(opcion == 2):
        a=np.arange(puntoInicial,puntoFinal,paso)
        a=np.arange(puntoInicial,puntoFinal,paso)
        b=[Funcion_f(f,a[ai]) for ai in range(len(a))]
        plt.plot(a,b,label='f(x)')
        b=[funcion2.subs(x,a[ai]) for ai in range(len(a))]
        plt.plot(a,b,label='g(x)')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Funcion f(x) y g(x)')
        plt.autoscale()
        plt.grid()
        plt.legend(loc=1)
        plt.savefig('GottaGoFast\static\images\img.png')
        plt.delaxes()

if __name__ == '__main__':
    app.run(debug=True)