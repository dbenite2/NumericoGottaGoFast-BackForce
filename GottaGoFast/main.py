from __future__ import division
from flask import Flask, request, render_template,redirect,url_for
from flask_caching import Cache
from sympy import * 
import matplotlib.pyplot as plt
import pylab
import sympy as sy
import numpy as np
import math
from sympy import *
from sympy.parsing.sympy_parser import parse_expr,convert_xor,standard_transformations,implicit_multiplication,implicit_application,function_exponentiation,factorial_notation,rationalize
import os
from math import pi

f = Function('fx')
X = Symbol('x')
transformations = standard_transformations + (convert_xor,implicit_multiplication,implicit_application)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def paginaPrincipal():
    return render_template("inicio.html")

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


@app.route('/busquedasIncrementales', methods=['GET','POST'])
def Busquedas_incrementales():
    global f
    x = Symbol('x')
    metodo = request.form.get('selector1')
    if (metodo == "0") or (metodo == "busquedasIncrementales"):
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
        fx0 = Funcion_f(f,x0)
        if fx0 == 0:
            graficar(0,f,'',puntoInicial,'',delta/10)
            return render_template('busquedasIncrementales.html', grafica = 1 ,x1 = x0, raiz = 1, error = 0, fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
        else:
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

@app.route('/biseccion', methods=['GET','POST'])
def Biseccion():
    global f
    metodo = request.form.get('selector1')
    e = int(request.form.get('selector2'))
    if (metodo == "0") or (metodo == "biseccion"):
        x = Symbol('x')
        ejecuciones = []
        f = parse_expr(request.form.get('fx'),transformations=transformations)
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
        fxi = Funcion_f(f,xi)
        fxs = Funcion_f(f,xs)
        graficar(1,f,'',puntoInicial, puntoFinal,abs((puntoInicial-puntoFinal)/100))
        if fxi == 0:
            return render_template('biseccion.html', grafica = 1 , error = 0, raiz = 1, xm = xi, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs == 0:
            return render_template('biseccion.html',grafica = 1 , error = 0, raiz = 1, xm = xs, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif fxs*fxi > 0:
            return render_template('biseccion.html', grafica = 1 , error = 1, mensajeError = 'En el intervalor ingresado no hay ninguna raiz', tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        else:
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

@app.route('/reglaFalsa', methods=['GET','POST'])
def Regla_falsa():
    global f
    metodo = request.form.get('selector1')
    e = int(request.form.get('selector2'))
    if (metodo == "0")  or (metodo == "reglaFalsa"):
        x = Symbol('x')
        ejecuciones = []
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
        print('FXI')
        fxi = Funcion_f(f,xi)
        print('FXs')
        fxs = Funcion_f(f,xs)
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

@app.route('/puntoFijo',methods = ['GET','POST'])
def Punto_fijo():
    global f 
    metodo = request.form.get('selector1')
    e = int(request.form.get('selector2'))
    if(metodo == "0" or metodo == "puntoFijo"):
        ejecuciones = []
        f = parse_expr(request.form.get('fx'),transformations=transformations)
        g = parse_expr(request.form.get('gx'),transformations=transformations)
        x0 = float(request.form.get('x0'))
        tol = float(request.form.get('tol'))
        ite = int(request.form.get('ite'))
        if tol == 0:
            return render_template('puntoFijo.html', error = 1, tol = request.form.get('tol'), mensaje_error = 'La tolerancia debe ser diferente de 0', fx = request.form.get('fx'), gx = request.form.get('gx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        ite = int(request.form.get('ite'))
        if ite <= 0: 
            return render_template('puntoFijo.html', error = 1, tol = request.form.get('tol'), mensaje_error = 'El número de iteraciones debe ser mayor a 0', fx = request.form.get('fx'), gx = request.form.get('gx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        puntoInicial = x0
        primerPunto = x0
        fxa = Funcion_f(f,x0)
        contador = 0
        error = tol + 1
        ejecuciones.append([contador, x0, "{:+.2e}".format(fxa),'No Hay'])
        while fxa != 0 and error > tol and contador < ite:
            print("empieza ejecución")
            print("Función g: ",g)
            xn = Funcion_f(g,x0)
            print("xn: ", xn)
            fxa = Funcion_f(f,x0)
            print("fxa: ", fxa)
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

@app.route('/newton', methods = ['GET','POST'])
def Newton():
    global f
    metodo = request.form.get('selector1')
    e = int(request.form.get('selector2'))
    if(metodo == "0" or metodo == "newton"):
        ejecuciones = []
        f = parse_expr(request.form.get('fx'),transformations=transformations)
        x0 = float(request.form.get('x0'))
        tol = float(request.form.get('tol'))
        if tol == 0:
            return render_template('newton.html', error = 1, tol = request.form.get('tol'), mensaje_error = 'La tolerancia debe ser diferente de 0', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        ite = int(request.form.get('ite'))
        if ite <= 0: 
            return render_template('newton.html', error = 1, tol = request.form.get('tol'), mensaje_error = 'El número de iteraciones debe ser mayor a 0', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        puntoInicial = x0
        primerPunto = x0
        fx0 = Funcion_f(f,x0)
        dfx0 = Funcion_p(f,x0)
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

@app.route('/secante', methods=['GET','POST'])
def Secante():
    global f
    metodo = request.form.get('selector1')
    e = int(request.form.get('selector2'))
    if (metodo == "0")  or (metodo == "secante"):
        # x = Symbol('x')
        ejecuciones = []
        f = parse_expr(request.form.get('fx'),transformations=transformations)
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

@app.route('/raicesMultiples', methods = ['GET','POST'])
def Raices_multiples():
    global f
    metodo = request.form.get('selector1')
    e = int(request.form.get('selector2'))
    if (metodo == "0") or (metodo == "raicesMultiples"):
        ejecuciones = []
        f = parse_expr(request.form.get('fx'),transformations=transformations)
        x0 = float(request.form.get('x0'))
        tol = float(request.form.get('tol'))
        if tol == 0:
            return render_template('raicesMultples.html', error = 1, tol = request.form.get('tol'), mensaje_error = 'La toleraciona debe de ser diferente de 0', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        ite = int(request.form.get('ite'))
        if ite <= 0:
            return render_template('raicesMultples.html', error = 1, tol = request.form.get('tol'), mensaje_error = 'El número de iteraciones debe de ser mayor a 0', fx = request.form.get('fx'), x0 = request.form.get('x0'), ite = request.form.get('ite'))
        puntoInicial = x0
        primerPunto = x0
        fx0 = Funcion_f(f,x0)
        dfx0 = Funcion_p(f,x0)
        d2fx0 = Funcion_p2(f,x0)
        den = (dfx0**2) - (fx0*d2fx0)
        error = tol + 1 
        contador = 0
        ejecuciones.append([contador, x0, "{:+.2e}".format(fx0), 'No Hay', 'No Hay'])
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