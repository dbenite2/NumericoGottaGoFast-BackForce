from __future__ import division
from flask import Flask, request, render_template,redirect,url_for
from sympy import * 
import matplotlib.pyplot as plt
import pylab
import sympy as sy
import numpy as np
import math
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import os

f = Function('fx')
X = Symbol('x')

app = Flask(__name__)

@app.route('/busquedasIncrementales')
def busquedas_incrementales():
    return render_template("busquedasIncrementales.html")

@app.route('/biseccion')
def biseccion():
    return render_template("biseccion.html")

@app.route('/reglaFalsa')
def reglaFalsa():
    return render_template("reglaFalsa.html")

# falta implementacion completa 
@app.route('/puntoFijo')
def puntoFijo():
    return render_template("puntoFijo.html")
#falta vista
@app.route('/newton') 
def newton():
    return render_template("newton.html")
#falta vista
@app.route('/raicesMultiples')
def raices():
    return render_template("raicesMultiples.html")
 

@app.route('/secante')
def secante():
    return render_template("secante.html")

@app.route('/newton', methods = ['GET','POST'])
def Newton():
    global f
    metodo = request.form.get('selector1')
    if(metodo == "0" or metodo == "newton"):
        x = Symbol('x')
        ejecuciones = []
        f = parse_expr(request.form.get('fx'))
        x0 = float(request.form.get('x0'))
        tol = float(request.form.get('tol'))
        if tol == 0:
            return render_template('newton.html', error = 1, tol = request.form.get('tol'), mensaje_error = 'La tolerancia debe ser diferente de 0', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        ite = int(request.form.get('ite'))
        if ite <= 0: 
            return render_template('newton.html', error = 1, tol = request.form.get('tol'), mensaje_error = 'El número de iteraciones debe ser mayor a 0', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        
        fx0 = Funcion_f(f,x0)
        dfx0 = Funcion_p(f,x0)
        error_abs = tol + 1
        contador = 0
        ejecuciones.append([contador, x0, fx0, dfx0, 'No Hay', 'No Hay'])
        while fx0 != 0 and dfx0 != 0 and error_abs > tol and contador < ite:
            x1 = x0 - (fx0/dfx0)
            fx0 = Funcion_f(f,x1)
            dfx0 = Funcion_p(f,x1)
            error_abs = abs(x1 - x0)
            error_rel = abs(error_abs/x1)
            contador += 1 
            x0 = x1
            ejecuciones.append([contador, x0, fx0, dfx0, error_abs,error_rel])
        if fx0 == 0:
            return render_template('newton.html', raiz = 2, xs = x0, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        elif error_abs < tol:
            return render_template('newton.html', raiz = 3, xs = x0, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        elif dfx0 == 0:
            return render_template('newton.html', raiz = 4, xs = x0, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        else:
            return render_template('newton.html', raiz = 0, xs = x0, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
    else:
        if (metodo == "reglaFalsa") or (metodo == "secante") or (metodo == "biseccion"):
            f = parse_expr(request.form.get('fx'))
            xi = float(request.form.get('xinf'))
            xs = float(request.form.get('xsup'))
            tol = float(request.form.get('tol'))
            ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f, xinf = xi, xsup = xs, tol = tol, ite = ite)
        elif (metodo == "puntoFijo")  or (metodo == "raicesMultiples") or (metodo == "busquedasIncrementales"):
            f = parse_expr(request.form.get('fx'))
            xi = float(request.form.get('xinf'))
            tol = float(request.form.get('tol'))
            ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f, x0 = xi, tol = tol, ite = ite, x0i = xi)

@app.route('/raicesMultiples', methods = ['GET','POST'])
def Raices_multiples():
    global f
    metodo = request.form.get('selector1')
    if (metodo == 0) or (metodo == "raicesMultiples"):
        ejecuciones = []
        x0 = float(request.form.get('x0'))
        tol = float(request.form.get('tol'))
        if tol == 0:
            return render_template('raicesMultples.html', error = 1, tol = request.form.get('tol'), mensaje_error = 'La toleraciona debe de ser diferente de 0', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        ite = int(request.form.get('ite'))
        if ite <= 0:
            return render_template('raicesMultples.html', error = 1, tol = request.form.get('tol'), mensaje_error = 'El número de iteraciones debe de ser mayor a 0', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        fx0 = Funcion_f(f,x0)
        dfx0 = Funcion_p(f,x0)
        d2fx0 = Funcion_p(dfx0,x0)
        den = (dfx0**2) - (fx0*d2fx0)
        error_abs = tol + 1 
        contador = 0
        ejecuciones.append([contador, x0, fx0, dfx0, d2fx0, 'No Hay', 'No Hay'])
        while (fx0 != 0) and (error_abs > tol) and (den != 0) and contador < ite:
            den = (dfx0**2) - (fx0*d2fx0)
            x1 = x0 - ((fx0 * dfx0) / den)
            fx0 = Funcion_f(f,x1)
            dfx0 = Funcion_p(f,x1)
            d2fx0 = Funcion_p(dfx0,x1)
            error_abs = (x1 - x0)
            error_rel = (error_abs/x1)
            contador += 1
            x0 = x1
            ejecuciones.append([contador, x0, fx0, dfx0, d2fx0 , error_abs, error_rel])
        if fx0 == 0:
            return render_template('raicesMultiples.html', raiz = 2, xs = x0, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        elif error_abs < tol:
            return render_template('raicesMultiples.html', raiz = 3, xs = x0, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        elif dfx0 == 0:
            return render_template('raicesMultiples.html', raiz = 4, xs = x0, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        else:
            return render_template('raicesMultiples.html', raiz = 0, xs = x0, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
    else:
        if (metodo == "reglaFalsa") or (metodo == "secante") or (metodo == "biseccion"):
            f = parse_expr(request.form.get('fx'))
            xi = float(request.form.get('xinf'))
            xs = float(request.form.get('xsup'))
            tol = float(request.form.get('tol'))
            ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f, xinf = xi, xsup = xs, tol = tol, ite = ite)
        elif (metodo == "puntoFijo")  or (metodo == "newton") or (metodo == "busquedasIncrementales"):
            f = parse_expr(request.form.get('fx'))
            xi = float(request.form.get('xinf'))
            tol = float(request.form.get('tol'))
            ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f, x0 = xi, tol = tol, ite = ite, x0i = xi)

@app.route('/secante', methods=['GET','POST'])
def Secante():
    global f
    metodo = request.form.get('selector1')
    if (metodo == "0")  or (metodo == "secante"):
        # x = Symbol('x')
        ejecuciones = []
        f = parse_expr(request.form.get('fx'))
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
        fxi = Funcion_f(f,xi)
        fxs = Funcion_f(f,xs)
        if fxi == 0:
            return render_template('secante.html', error = 0, raiz = 1, xm = xi, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs == 0:
            return render_template('secante.html', error = 0, raiz = 1, xm = xs, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs*fxi > 0:
            return render_template('secante.html', error = 1, mensajeError = 'En el intervalor ingresado no hay ninguna raiz', tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        else:
            contador = 0
            errorAbs = tol + 1
            denominador = fxs - fxi
            ejecuciones.append([contador, xi, fxi, xs, fxs, 'No Hay', 'No Hay'])
            while fxs != 0 and errorAbs > tol and denominador != 0 and contador < ite:
                xn = xs - fxs*(xs-xi)/denominador
                errorAbs = abs(xn - xs)
                errorRel = abs(errorAbs/xn)
                xi = xs
                fxi = fxs
                xs = xn
                fxs = Funcion_f(f,xs)
                denominador = fxs - fxi     
                contador += 1
                ejecuciones.append([contador, xi, fxi, xs, fxs, errorAbs, errorRel]) 
            if fxs == 0:
                return render_template('secante.html', raiz = 2, xm = xs, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            elif errorAbs < tol:
                return render_template('secante.html', raiz = 3, xm = xs, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            elif denominador == 0 :
                return render_template('secante.html', raiz = 4, xm = xs, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            else:
                return render_template('secante.html', raiz = 0, xm = xs, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
    else:
        if (metodo == "biseccion") or (metodo == "reglaFalsa"):
            f = parse_expr(request.form.get('fx'))
            xi = float(request.form.get('xinf'))
            xs = float(request.form.get('xsup'))
            tol = float(request.form.get('tol'))
            ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f, xinf = xi, xsup = xs, tol = tol, ite = ite)
        elif (metodo == "puntoFijo") or (metodo == "newton") or (metodo == "raicesMultiples") or (metodo == "busquedasIncrementales"):
            f = parse_expr(request.form.get('fx'))
            xi = float(request.form.get('xinf'))
            tol = float(request.form.get('tol'))
            ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f, x0 = xi, tol = tol, ite = ite, x0i = xi)

@app.route('/reglaFalsa', methods=['GET','POST'])
def Regla_falsa():
    global f
    metodo = request.form.get('selector1')
    if (metodo == "0")  or (metodo == "reglaFalsa"):
        x = Symbol('x')
        ejecuciones = []
        f = parse_expr(request.form.get('fx'))
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
        fxi = Funcion_f(f,xi)
        fxs = Funcion_f(f,xs)
        if fxi == 0:
            return render_template('reglaFalsa.html', error = 0, raiz = 1, xm = xi, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs == 0:
            return render_template('reglaFalsa.html', error = 0, raiz = 1, xm = xs, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs*fxi > 0:
            return render_template('reglaFalsa.html', error = 1, mensajeError = 'En el intervalor ingresado no hay ninguna raiz', tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        else:
            xm = xi - (fxi*(xs-xi))/(fxs-fxi)
            fxm = Funcion_f(f,xm)
            ejecuciones.append([0, xi, fxi, xs, fxs, xm, fxm, 'No Hay', 'No Hay'])
            contador = 1
            errorAbs = tol + 1
            while fxm != 0 and errorAbs > tol and contador < ite:
                if fxi * fxm < 0:
                    xs = xm
                    fxs = Funcion_f(f,xs)
                else:
                    xi = xm
                    fxi = Funcion_f(f,xi)
                xmAnt = xm
                xm = xi - (fxi*(xs-xi))/(fxs-fxi)
                fxm = Funcion_f(f,xm)
                errorAbs = abs(xm - xmAnt)
                errorRel = errorAbs/xm
                ejecuciones.append([contador, xi, fxi, xs, fxs, xm, fxm, errorAbs, errorRel])
                contador = contador + 1
            if fxm == 0:
                return render_template('reglaFalsa.html', raiz = 2, xm = xm, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            elif errorAbs < tol:
                return render_template('reglaFalsa.html', raiz = 3, xm = xm, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            else:
                return render_template('reglaFalsa.html', raiz = 0, xm = xm, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
    else:
        if (metodo == "biseccion") or (metodo == "secante"):
            f = parse_expr(request.form.get('fx'))
            xi = float(request.form.get('xinf'))
            xs = float(request.form.get('xsup'))
            tol = float(request.form.get('tol'))
            ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f, xinf = xi, xsup = xs, tol = tol, ite = ite)
        elif (metodo == "puntoFijo") or (metodo == "newton") or (metodo == "raicesMultiples") or (metodo == "busquedasIncrementales"):
            f = parse_expr(request.form.get('fx'))
            xi = float(request.form.get('xinf'))
            tol = float(request.form.get('tol'))
            ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f, x0 = xi, tol = tol, ite = ite, x0i = xi)

@app.route('/biseccion', methods=['GET','POST'])
def Biseccion():
    global f
    metodo = request.form.get('selector1')
    if (metodo == "0") or (metodo == "biseccion"):
        x = Symbol('x')
        ejecuciones = []
        f = parse_expr(request.form.get('fx'))
        xi = float(request.form.get('xinf'))
        xs = float(request.form.get('xsup'))
        if xi == xs:
            return render_template('biseccion.html', error = 1, tol = request.form.get('tol'), mensajeError = 'El intervalo es invalido', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        tol = float(request.form.get('tol'))
        if tol == 0:
            return render_template('biseccion.html', error = 1, tol = request.form.get('tol'), mensajeError = 'La tolerancia debe ser diferente de 0', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        ite = int(request.form.get('ite'))
        if ite <= 0:
            return render_template('biseccion.html', error = 1, tol = request.form.get('tol'), mensajeError = 'El numero de iteraciones debe ser mayor a 0', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        fxi = Funcion_f(f,xi)
        fxs = Funcion_f(f,xs)
        if fxi == 0:
            return render_template('biseccion.html', error = 0, raiz = 1, xm = xi, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs == 0:
            return render_template('biseccion.html', error = 0, raiz = 1, xm = xs, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs*fxi > 0:
            return render_template('biseccion.html', error = 1, mensajeError = 'En el intervalor ingresado no hay ninguna raiz', tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        else:
            xm = (xi + xs) / 2
            fxm = Funcion_f(f,xm)
            ejecuciones.append([0,str(xi),str(fxi),str(xs),str(fxs),str(xm),str(fxm),'No Hay','No Hay'])
            contador = 1
            errorAbs = tol + 1
            while fxm != 0 and errorAbs > tol and contador < ite:
                if fxi * fxm < 0:
                    xs = xm
                    fxs = Funcion_f(f,xs)
                else:
                    xi = xm
                    fxi = Funcion_f(f,xi)
                xmAnt = xm
                xm = (xi + xs) / 2
                fxm = Funcion_f(f,xm)
                errorAbs = abs(xm - xmAnt)
                errorRel = errorAbs/xm
                ejecuciones.append([contador,xi,fxi,xs,fxs,xm,fxm,errorAbs,errorRel])
                contador = contador + 1
            if fxm == 0:
                return render_template('biseccion.html', raiz = 2, xm = xm, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            elif errorAbs < tol:
                return render_template('biseccion.html', raiz = 3, xm = xm, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
            else:
                return render_template('biseccion.html', raiz = 0, xm = xm, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
    else:
        if (metodo == "reglaFalsa") or (metodo == "secante"):
            f = parse_expr(request.form.get('fx'))
            xi = float(request.form.get('xinf'))
            xs = float(request.form.get('xsup'))
            tol = float(request.form.get('tol'))
            ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f, xinf = xi, xsup = xs, tol = tol, ite = ite)
        elif (metodo == "puntoFijo") or (metodo == "newton") or (metodo == "raicesMultiples") or (metodo == "busquedasIncrementales"):
            f = parse_expr(request.form.get('fx'))
            xi = float(request.form.get('xinf'))
            tol = float(request.form.get('tol'))
            ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f, x0 = xi, tol = tol, ite = ite, x0i = xi)

@app.route('/busquedasIncrementales', methods=['GET','POST'])
def Busquedas_incrementales():
    global f
    metodo = request.form.get('selector1')
    if (metodo == "0") or (metodo == "busquedasIncrementales"):
        ejecuciones = []
        f = parse_expr(request.form.get('fx'))
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
        fx0 = Funcion_f(f,x0)
        if fx0 == 0:
            graficar(0,f,puntoInicial,'')
            return render_template('busquedasIncrementales.html', grafica = 1 ,x1 = x0, raiz = 1, error = 0, fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
        else:
            x1 = x0 + delta
            fx1 = Funcion_f(f,x1)
            contador = 1
            ejecuciones.append([0,str(x0),str(fx0)])
            while fx0*fx1 > 0 and contador < ite:
                fx0 = fx1
                x0 = x1
                x1 = x1 + delta
                fx1 = Funcion_f(f,x1)
                ejecuciones.append([contador,str(x0),str(fx0)])
                contador += 1
            if fx1 == 0:
                fx0 = fx1
                x0n = x1
                ejecuciones.append([contador,str(x0n),str(fx0)])
                #graficar(1,f,puntoInicial,x0n)
                return render_template('busquedasIncrementales.html', grafica = 1, x1 = x1, raiz = 2, error = 0,ejecuciones = ejecuciones, fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
            elif (fx0 * fx1) < 0:
                fx0 = fx1
                x0n = x1
                #graficar(1,f,puntoInicial,x0n)
                ejecuciones.append([contador,x0n,fx0])
                return render_template('busquedasIncrementales.html', grafica = 1, n = contador, ejecuciones = ejecuciones, raiz = 3, error = 0, x0 = x0, x1 = x1,fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
            else: 
                fx0 = fx1
                x0n = x1
                #graficar(1,f,puntoInicial,x0n)
                ejecuciones.append([contador,str(x0n),str(fx0)])
                return render_template('busquedasIncrementales.html', grafica = 1, n = contador, ejecuciones = ejecuciones, raiz = 0, error = 0, x0 = x0, x1 = x1, fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
    else:
        if (metodo == "biseccion") or (metodo == "reglaFalsa") or (metodo == "secante"):
            f = parse_expr(request.form.get('fx'))
            x0 = float(request.form.get('x0'))
            ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f, xinf = x0, ite = ite)
        elif (metodo == "puntoFijo") or (metodo == "newton") or (metodo == "raicesMultiples"):
            f = parse_expr(request.form.get('fx'))
            x0 = float(request.form.get('x0'))
            ite = int(request.form.get('ite'))
            return render_template(metodo + ".html", fx = f, x0 = x0, ite = ite, x0i = x0)


@app.route('/')
def paginaPrincipal():
    return '<h1>Aqui va la pagina principal</h1>'

def Funcion_f(fx,entrada):
    x = entrada
    fx = str(fx)
    print("fx: ",fx)
    print("eval: ", eval(fx))
    return eval(fx)

def Funcion_p(fx,entrada):
    fpx = str(diff(fx,X))
    x = entrada
    return eval(fpx)

def Funcion_p2(fx,entrada):
    fp2x = str(diff(fx,X,2))
    x = entrada
    return eval(fp2x)

def graficar(opcion, funcion, puntoInicial,puntoFinal):
    os.remove('static/images/img.png')
    global f
    x = Symbol('x')
    if(opcion == 0):
        a=np.arange(puntoInicial-2,puntoInicial+2.1,0.1)
        b=[funcion.subs(x,a[ai]) for ai in range(len(a))]
        plt.plot(a,b,label='f(x)')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Funcion f(x)')
        plt.autoscale()
        plt.grid()
        plt.legend(loc=1)
        plt.savefig('static/images/img.png')
        plt.delaxes()
    elif(opcion == 1):
        a=np.arange(puntoInicial,puntoFinal+0.1,0.1)
        b=[funcion.subs(x,a[ai]) for ai in range(len(a))]
        plt.plot(a,b,label='f(x)')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Funcion f(x)')
        plt.autoscale()
        plt.grid()
        plt.legend(loc=1)
        plt.savefig('static/images/img.png')
        plt.delaxes()

if __name__ == '__main__':
    app.run(debug=True)