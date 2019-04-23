from flask import Flask, request, render_template,redirect,url_for
from sympy import * 
import sympy as sy
import numpy as np
import math

iteracion = []
X0 = []
X1 = []
FX = []
DFX = []
Error = []

X = Symbol('x')

app = Flask(__name__)

@app.route('/')
def paginaPrincipal():
    return '<h1>Aqui va la pagina principal</h1>'

@app.route('/metodos', methods=['GET','POST'])
def metodos():
    if request.method == 'POST':
        #datos generales para los metodos
        fx = request.form.get('fx')
        intervalo = request.form.get('selectIntervalos')
        metodo = request.form.get('selectMetodo')
        #datos para busqueda incremental
        x0b = request.form.get('x0b')
        deltab = request.form.get('deltab')
        iteb = request.form.get('iteb')
        #datos para biseccion y regla falsa
        
        xinfbr = request.form.get('xinfbr')
        xsupbr = request.form.get('xsupbr')
        tolbr = request.form.get('tolbr')
        itebr = request.form.get('itebr')
        #datos para punto fijo
        fgx = request.form.get('fgx') 
        x0npr = request.form.get('x0f')
        tolnpr = request.form.get('tolf')
        itenpr = request.form.get('itef')
        #datos para newton y raices multiples
        x0npr = request.form.get('x0npr')
        print ( "x0: ", x0npr)
        tolnpr = request.form.get('tolnpr')
        itenpr = request.form.get('itenpr')
        #datos para secante
        x0s = request.form.get('x0s')
        x1s = request.form.get('x1s')
        tols = request.form.get('tols')
        ites = request.form.get('ites')

        if intervalo == 'Si':
            return redirect(url_for('busquedas',fx = fx,x0b = x0b, deltab = deltab, iteb = iteb, **request.args))
        
        elif metodo == '1':
            return redirect(url_for('biseccion',fx = fx, xinfbr = xinfbr, xsupbr = xsupbr, tolbr = tolbr, itebr = itebr, **request.args ))
        elif metodo == '2':
            return redirect(url_for('reglaFalsa',fx = fx, xinfbr = xinfbr, xsupbr = xsupbr, tolbr = tolbr, itebr = itebr, **request.args ))
        elif metodo == '3':
            return redirect(url_for('puntoFijo',fx = fx, fgx = fgx, x0f = x0f, tolf = tolf, itef = itef, **request.args))
        elif metodo == '4':
            return redirect(url_for('newton',fx = fx, x0npr = x0npr, tolnpr = tolnpr, itenpr = itenpr, **request.args))
        elif metodo == '5':
            return redirect(url_for('secante', fx = fx, x0s = x0s, x1s = x1s, tols = tols, ites = ites, **request.args))
        elif metodo == '6':
            return redirect(url_for('raicesm',fx = fx, x0npr = x0npr, tolnpr = tolnpr, itenpr = itenpr, **request.args))

        return render_template("metodos.html", fx=fx,intervalo=intervalo,metodo=metodo,x0b=x0b,deltab=deltab,iteb=iteb,xinfbr=xinfbr,xsupbr=xsupbr,tolbr=tolbr,itebr=itebr,x0npr=x0npr,tolnpr=tolnpr,itenpr=itenpr,x0s=x0s,x1s=x1s,tols=tols,ites=ites)
    elif request.method == 'GET':
        return render_template("metodos.html")

#Metodo de busquedas incrementales   
@app.route('/busquedas')
def busquedas():

    limpiar()

    fx    = request.args['fx']
    x0    = float(request.args['x0b'])
    delta =  float(request.args['deltab'])
    iteb  = int(request.args['iteb'])

    fx0 = funcion(fx,x0)

    # print('{:30},{:30},{:30}'.format('n','x0','f(x0)'))
    if fx0 == 0:
        return render_template('raizUnica.html',x1 = x0)
    else:
        #lista.append([contador, x0, fx0])
        x1 = x0 + delta
        fx1 = funcion(fx,x1)
        contador = 1
        ##tabla.append([0,x0,fx0])
        # print('{:30},{:30},{:30}'.format(str(0),str(x0),str(fx0)))
        while (fx0 * fx1) > 0 and contador <= iteb:
            #fx1 = fx0
            x0 = x1
            fx0 = fx1
            #lista.append([contador, x0, fx0])
            x1 = x1 + delta
            fx1 = funcion(fx,x1)
            ##tabla.append([contador,x0,fx0])
            #print('{:30},{:30},{:30}'.format(str(contador),str(x0),str(fx0)))
            contador += 1
        ##tabla.append([contador,x1,fx1])
        # print('{:30},{:30},{:30}'.format(str(contador),str(x1),str(fx1)))    
        #lista.append([contador,x1,fx1])
        if fx1 == 0:
            return render_template('raizUnica.html',x1 = x1, tablaM = tabla)
        elif (fx0 * fx1) < 0:
            print ("Hay una raiz entre ", x0, " y ", x1)
            return render_template('Busquedas.html',x0 = x0, x1 = x1 , n = contador, fx0 = fx0, fx1 = fx1, tablaM = tabla)
        else : 
            return render_template('errores.html',n = contador, tablaM = tabla)

#Metodo de biseccion
@app.route('/biseccion')
def biseccion():

    limpiar()

    fx = request.args['fx']
    xinf = float(request.args['xinfbr'])
    xsup = float(request.args['xsupbr'])
    tol  = float(request.args['tolbr'])
    ite  = int(request.args['itebr'])

    fxinf = funcion(fx,xinf)
    fxsup = funcion(fx,xsup)

    if fxinf == 0:
        return render_template('raizUnica.html',x1 = xinf)
    elif fxsup == 0:
        return render_template('raizUnica.html',x1 = xsup)
    elif (fxinf * fxsup) < 0:
        xm = (xinf + xsup) / 2
        fxm = funcion(fx,xm)
        contador = 1
        error = tol + 1
        ##tabla.append([contador,xinf,xsup,xm,fxm,error])
        # print('{:30},{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(xinf),str(xsup),str(xm),str(fxm),str(error)))

        while fxm != 0 and error > tol and contador < ite:
            if (fxinf * fxm) < 0:
                xsup = xm
                fxsup = fxm
            else:
                xinf = xm
                fxinf = fxm
            temp = xm 
            xm = (xinf + xsup) / 2
            fxm = funcion(fx,xm)
            error = math.fabs(xm - temp)
            ##tabla.append([contador,xinf,xsup,xm,fxm,error])
            # print('{:30},{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(xinf),str(xsup),str(xm),str(fxm),str(error)))
            contador += 1
        ##tabla.append([contador,xinf,xsup,xm,fxm,error])
        # print('{:30},{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(xinf),str(xsup),str(xm),str(fxm),str(error)))
        if fxm == 0:
            return render_template('raizUnica.html',x1 = xm, tablaM = tabla)
        elif error < tol:
            return render_template('biseccion.html', n = contador, xm = xm, tol = tol,fx0 = fxm, tablaM = tabla)
        else:
            return render_template('errores.html', n = contador, tablaM = tabla)
    else:
            return render_template('errores.html', tablaM = tabla)



@app.route('/reglaFalsa')
def reglaFalsa():

    limpiar()

    fx = request.args['fx']
    xinf = float(request.args['xinfbr'])
    xsup = float(request.args['xsupbr'])
    tol  = float(request.args['tolbr'])
    ite  = int(request.args['itebr'])

    fxinf = funcion(fx,xinf)
    fxsup = funcion(fx,xsup)

    if fxinf == 0:
        return render_template('raizUnica.html',x1 = xinf)
    elif fxsup == 0:
        return render_template('raizUnica.html',x1 = xsup)
    elif (fxinf * fxsup) < 0:
        xm = xinf - ((fxinf * (xsup - xinf) / (fxsup - fxinf)))
        fxm = funcion(fx,xm)
        contador = 1
        error = tol + 1
        ##tabla.append([contador,xinf,xsup,xm,fxm,error])
        # print('{:30},{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(xinf),str(xsup),str(xm),str(fxm),str(error)))

        while fxm != 0 and error > tol and contador < ite:
            if (fxinf * fxm) < 0:
                xsup = xm
                fxsup = fxm
            else:
                xinf = xm
                fxinf = fxm
            temp = xm 
            xm = xinf - ((fxinf * (xsup - xinf) / (fxsup - fxinf)))
            fxm = funcion(fx,xm)
            error = math.fabs(xm - temp)
            ##tabla.append([contador,xinf,xsup,xm,fxm,error])
            # print('{:30},{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(xinf),str(xsup),str(xm),str(fxm),str(error)))
            contador += 1
        ##tabla.append([contador,xinf,xsup,xm,fxm,error])
        # print('{:30},{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(xinf),str(xsup),str(xm),str(fxm),str(error)))
        if fxm == 0:
            return render_template('raizUnica.html',x1 = xm, tablaM = tabla)
        elif error < tol:
            return render_template('biseccion.html', n = contador, xm = xm, tol = tol,fx0 = fxm, tablaM = tabla)
        else:
            return render_template('errores.html', n = contador, tablaM = tabla)
    else:
            return render_template('errores.html', tablaM = tabla)    
        
@app.route('/puntoFijo')
def puntoFijo():

    limpiar()
    
    fx  = request.args['fx']
    fgx = request.args['fgx']
    x0  = float(request.args['x0f'])
    tol = float(request.args['tolf'])
    ite = int(request.args['itef'])

    fxa = funcion(fx,x0)
    contador = 0
    error = tol + 1
    # print('{:30},{:30},{:30},{:30}'.format('n','xn','fxn','error'))
    while fxa != 0 and error > tol and contador < ite:
        xn = funcion(fgx,x0) 
        fxa = funcion(fx,xn)
        error =  math.fabs(xn-x0)
        x0 = xn 
        ##tabla.append([contador,xn,fx,error])
        # print('{:30},{:30},{:30},{:30}'.format(str(contador),str(xn),str(fx),str(error)))
        contador += 1
    #tabla.append([contador,xn,fx,error])
    #print('{:30},{:30},{:30},{:30}'.format(str(contador),str(xn),str(fx),str(error)))
    if fxa == 0:
        return render_template('raizUnica.html',x1 = x0, tablaM = tabla)
    else:
        if error < tol:
            return render_template('biseccion.html', n = contador, xm = x0, tol = tol,fx0 = fxa, tablaM = tabla)
            
            #print(error_type)
        else:
           return render_template('errores.html', n = contador, tablaM = tabla)



@app.route('/newton')
def newton():

    iteracion = []
    X0 = []
    X1 = []
    FX = []
    DFX = []
    Error = []
    
    fx  = request.args['fx']
    print("error", request.args['x0npr'])
    x0  = float(request.args['x0npr'])
    tol = float(request.args['tolnpr'])
    ite = int(request.args['itenpr'])
    
    fx0   = funcion(fx,x0)
    dfx0  = funcionP(fx,x0)
    error = tol + 1
    contador = 0
    # print('{:30},{:30},{:30},{:30},{:30}'.format('n','xn','f(xn)','d(xn)','error'))

    while error > tol and fx0 != 0 and dfx0 != 0 and contador < ite:
        x1 = x0 - (fx0/dfx0)
        fx0 = funcion(fx,x1)
        dfx0 = funcionP(fx,x1)
        error = math.fabs((x1 -x0)/x1)
        contador += 1
        x0 = x1
        iteracion.append(contador)
        X0.append(x0)
        FX.append(fx0)
        DFX.append(dfx0)
        Error.append(error)
        ##tabla.append([contador,x0, fx0, dfx0, error])
        # print('{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(x0),str(fx0),str(dfx0),str(error)))

    if fx0 == 0:
        return render_template('raizUnica.html',x1 = x0, iteracion = iteracion, X0 = X0, FX = FX, DFX = DFX, Error = Error)
    else:
        if error < tol:
           return render_template('biseccion.html', n = contador, xm = x1, tol = tol,fx0 = fx0, iteracion = iteracion, X0 = X0, FX = FX, DFX = DFX, Error = Error, len = len(iteracion))
        else:
            if dfx0 == 0:
                return render_template('multipleSolucion.html',x1 = x1, iteracion = iteracion, X0 = X0, FX = FX, DFX = DFX, Error = Error)
                 
            else:
                return render_template('errores.html', n = contador, iteracion = iteracion, X0 = X0, FX = FX, DFX = DFX, Error = Error)



@app.route('/secante')
def secante():

    limpiar()
    
    fx  = request.args['fx']
    x0  = float(request.args['x0s'])
    x1  = float(request.args['x1s'])
    tol = float(request.args['tols'])
    ite = int(request.args['ites'])

    fx0 = funcion(fx,x0) 

    # print('{:30},{:30},{:30},{:30}'.format('n', 'xn', 'f(xn)', 'error'))
    if fx0 == 0:
        return render_template('raizUnica.html',x1 = x0)
    else: 
        fx1 = funcion(fx,x1)
        error = tol + 1
        contador = 0
        denominador = fx1 - fx0
        while fx1 != 0 and error > tol and denominador != 0 and contador < ite:
            x2 = x1 - ((fx1 * (x1 - x0)) / denominador)
            error = math.fabs((x2 - x1)/x2)
            x0 = x1
            fx0 = fx1
            x1 = x2
            fx1 = funcion(fx,x1)
            denominador = fx1 - fx0
            ##tabla.append([contador,x1, fx1, error])
            # print('{:30},{:30},{:30},{:30}'.format(str(contador),str(x1),str(fx1),str(error)))
            contador += 1
        ##tabla.append([contador,x1, fx1, error])
        # print('{:30},{:30},{:30},{:30}'.format(str(contador),str(x1),str(fx1),str(error)))
        if fx1 == 0:
            return render_template('raizUnica.html',x1 = x1, tablaM = tabla)
        else:
            if error < tol:
                 return render_template('biseccion.html', n = contador, xm = x1, tol = tol,fx0 = fx1, tablaM = tabla)
            else:
                if denominador == 0:
                    return render_template('multipleSolucion.html',x1 = x1, tablaM = tabla)
                else: 
                    return render_template('errores.html', n = contador, tablaM = tabla)



@app.route('/raicesm')
def raicesm():

    limpiar()
    
    fx = request.args['fx']
    x0  = float(request.args['x0npr'])
    tol = float(request.args['tolnpr'])
    ite = int(request.args['itenpr'])
    
    fx0 = funcion(fx,x0)
    dfx0 = funcionP(fx,x0)
    d2fx0 = funcionP2(fx,x0)
    den = (dfx0**2) - (fx0*d2fx0)
    error = tol + 1
    contador = 0
    # print('{:30} {:30} {:30} {:30} {:30} {:30}'.format('Iterations', 'x', 'fx', 'dfx', 'd2f', 'error'))

    while (fx0 != 0) and (error > tol) and (den != 0)  and (contador < ite):
        den = (dfx0**2) - (fx0*d2fx0)
        x1 = x0 - ((fx0 * dfx0) / den)
        fx0 = funcion(fx,x1)
        dfx0 = funcionP(fx,x1)
        d2fx0 = funcionP2(fx,x1)
        error = math.fabs((x1 -x0)/x1)
        contador += 1
        x0 = x1
        ##tabla.append([contador,x0, fx0,dfx0,d2fx0, error])
        # print('{:30},{:30},{:30},{:30},{:30}'.format(str(contador),str(x0),str(fx0),str(dfx0),str(d2fx0),str(error)))

    if fx0 == 0:
        return render_template('raizUnica.html',x1 = x0, tablaM = tabla)
    else:
        if error < tol:
            return render_template('biseccion.html', n = contador, xm = x1, tol = tol,fx0 = fx1, tablaM = tabla)
        else:
            if dfx0 == 0:
                return render_template('multipleSolucion.html',x1 = x1, tablaM = tabla)
            elif d2fx0 == 0:
                return render_template('multipleSolucion.html',x1 = x1, tablaM = tabla)
            else:
                 return render_template('errores.html', n = contador, tablaM = tabla)

def limpiar():
    i = 0
    tam = len(iteracion)
    while i < tam :
        iteracion.pop()
        X0.pop()
        X1.pop()
        FX.pop()
        DFX.pop()
        Error.pop()

def funcion(fx,entrada):
    x = entrada
    return eval(fx)

def funcionP(fx,entrada):
    fpx = str(diff(fx,X))
    x = entrada
    return eval(fpx)

def funcionP2(fx,entrada):
    
    fp2x = str(diff(fx,X,2))
    x = entrada
    return eval(fp2x)

if __name__ == '__main__':
    app.run(debug=True)