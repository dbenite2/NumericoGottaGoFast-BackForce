from __future__ import division
from flask import Flask, request, render_template,redirect,url_for
from sympy import * 
import sympy as sy
import numpy as np
import math
from sympy import *
from sympy.parsing.sympy_parser import parse_expr

f = Function('fx')

app = Flask(__name__)

@app.route('/busquedasIncrementales')
def BusquedasIncrementales():
    return render_template("busquedasIncrementales.html")

@app.route('/biseccion')
def Biseccion():
    return render_template("biseccion.html")

@app.route('/reglaFalsa')
def ReglaFalsa():
    return render_template("reglaFalsa.html")

@app.route('/secante')
def Secante():
    return render_template("secante.html")

@app.route('/secante', methods=['GET','POST'])
def secante():
    global f
    x = Symbol('x')
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
        return render_template('secante.html', error = 1, tol = request.form.get('tol'), mensajeError = 'El numero de iteraciones debe ser mayor a 0', fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
    fxi = f.subs(x,xi)
    fxs = f.subs(x,xs)
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
            fxs = f.subs(x,xs)
            denominador = fxs - fxi
            ejecuciones.append([contador, xi, fxi, xs, fxs, errorAbs, errorRel])      
            contador += 1
        if fxs == 0:
            return render_template('secante.html', raiz = 2, xm = xs, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif errorAbs < tol:
            return render_template('secante.html', raiz = 3, xm = xs, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        elif denominador == 0 :
            return render_template('secante.html', raiz = 4, xm = xs, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
        else:
            return render_template('secante.html', raiz = 0, xm = xs, ejecuciones = ejecuciones, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))

@app.route('/reglaFalsa', methods=['GET','POST'])
def reglaFalsa():
    global f
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
    fxi = f.subs(x,xi)
    fxs = f.subs(x,xs)
    if fxi == 0:
        return render_template('reglaFalsa.html', error = 0, raiz = 1, xm = xi, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
    elif fxs == 0:
        return render_template('reglaFalsa.html', error = 0, raiz = 1, xm = xs, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
    elif fxs*fxi > 0:
        return render_template('reglaFalsa.html', error = 1, mensajeError = 'En el intervalor ingresado no hay ninguna raiz', tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
    else:
        xm = xi - (fxi*(xs-xi))/(fxs-fxi)
        fxm = f.subs(x,xm)
        ejecuciones.append([0, xi, fxi, xs, fxs, xm, fxm, 'No Hay', 'No Hay'])
        contador = 1
        errorAbs = tol + 1
        while fxm != 0 and errorAbs > tol and contador < ite:
            if fxi * fxm < 0:
                xs = xm
                fxs = f.subs(x,xs)
            else:
                xi = xm
                fxi = f.subs(x,xi)
            xmAnt = xm
            xm = xi - (fxi*(xs-xi))/(fxs-fxi)
            fxm = f.subs(x,xm)
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

@app.route('/biseccion', methods=['GET','POST'])
def biseccion():
    global f
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
    fxi = f.subs(x,xi)
    fxs = f.subs(x,xs)
    if fxi == 0:
        return render_template('biseccion.html', error = 0, raiz = 1, xm = xi, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
    elif fxs == 0:
        return render_template('biseccion.html', error = 0, raiz = 1, xm = xs, tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
    elif fxs*fxi > 0:
        return render_template('biseccion.html', error = 1, mensajeError = 'En el intervalor ingresado no hay ninguna raiz', tol = request.form.get('tol'), fx = request.form.get('fx'), xinf = request.form.get('xinf'), xsup = request.form.get('xsup'), ite = request.form.get('ite'))
    else:
        xm = (xi + xs) / 2
        fxm = f.subs(x,xm)
        ejecuciones.append([0,str(xi),str(fxi),str(xs),str(fxs),str(xm),str(fxm),'No Hay','No Hay'])
        contador = 1
        errorAbs = tol + 1
        while fxm != 0 and errorAbs > tol and contador < ite:
            if fxi * fxm < 0:
                xs = xm
                fxs = f.subs(x,xs)
            else:
                xi = xm
                fxi = f.subs(x,xi)
            xmAnt = xm
            xm = (xi + xs) / 2
            fxm = f.subs(x,xm)
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

@app.route('/busquedasIncrementales', methods=['GET','POST'])
def busquedasIncrementales():
    global f
    x = Symbol('x')
    ejecuciones = []
    f = parse_expr(request.form.get('fx'))
    x0 = float(request.form.get('x0'))
    delta = float(request.form.get('delta'))
    if delta == 0:
        return render_template('busquedasIncrementales.html', error = 1, mensajeError = 'El numero de pasos debe ser un numero diferente a 0', fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
    ite = int(request.form.get('ite'))
    if ite < 0:
        return render_template('busquedasIncrementales.html', error = 1, mensajeError = 'El numero de iteraciones debe ser mayor a 0',fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
    try:
        fx0 = f.subs(x,x0)
    except (ValueError, TypeError, NameError):
        return render_template('busquedasIncrementales.html', error = 1, mensajeError = 'Hay un error en la expresión ingresada',fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
    fx0 = f.subs(x,x0)
    if fx0 == 0:
        return render_template('busquedasIncrementales.html', x1 = x0, raiz = 1, error = 0, fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
    else:
        x1 = x0 + delta
        fx1 = f.subs(x,x1)
        contador = 1
        ejecuciones.append([0,str(x0),str(fx0)])
        while fx0*fx1 > 0 and contador < ite:
            fx0 = fx1
            x0 = x1
            x1 = x1 + delta
            fx1 = f.subs(x,x1)
            ejecuciones.append([contador,str(x0),str(fx0)])
            contador += 1
        if fx1 == 0:
            fx0 = fx1
            x0n = x1
            ejecuciones.append([contador,str(x0n),str(fx0)])
            return render_template('busquedasIncrementales.html',x1 = x1, raiz = 2, error = 0,ejecuciones = ejecuciones, fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
        elif (fx0 * fx1) < 0:
            fx0 = fx1
            x0n = x1
            ejecuciones.append([contador,x0n,fx0])
            return render_template('busquedasIncrementales.html',n = contador, ejecuciones = ejecuciones, raiz = 3, error = 0, x0 = x0, x1 = x1,fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))
        else: 
            fx0 = fx1
            x0n = x1
            ejecuciones.append([contador,str(x0n),str(fx0)])
            return render_template('busquedasIncrementales.html',n = contador, ejecuciones = ejecuciones, raiz = 0, error = 0, x0 = x0, x1 = x1, fx = request.form.get('fx'), x0i = request.form.get('x0'), delta = request.form.get('delta'), ite = request.form.get('ite'))


@app.route('/')
def paginaPrincipal():
    return '<h1>Aqui va la pagina principal</h1>'

if __name__ == '__main__':
    app.run(debug=True)