#!/usr/bin/python3

from sympy import *
import math
import sympy as sy
import numpy as np


def multipleRoots(tol, xa, niter):
    fx = f(xa)
    dfx = fd(xa)
    d2fx = d2f(xa)
    cont = 0
    error = tol + 1

    print('{:30} {:30} {:30} {:30} {:30} {:30}'.format('Iterations', 'x', 'fx', 'dfx', 'd2f', 'error'))

    while (((dfx * dfx) - fx * d2fx) != 0) and (fx != 0) and (error > tol) and (cont < niter) and (dfx != 0) and (
            d2fx != 0):
        xn = xa - ((fx * dfx) / ((dfx * dfx) - fx * d2fx))
        fx = f(xn)
        dfx = fd(xn)
        d2fx = d2f(xn)
        error = abs(xn - xa)
        xa = xn
        cont = cont + 1
        # print(cont, "         |", xa, "|", fx, "|", dfx, "|", d2fx, "|", error)
        print('{:30} {:30} {:30} {:30} {:30} {:30}'.format(str(cont), str(xa), str(fx), str(dfx), str(d2fx), str(error)))

    if fx == 0:
        print(str(xa) + " is a root")
    elif dfx == 0:
        print(str(xa) + " Is a possible multiple root ")
    elif d2fx == 0:
        print(str(xa) + " Is a possible multiple root ")
    elif error < tol:
        print(str(xa) + " Is a root aproximation with a tolerance of = " + str(tol))
    else:
        print("failure reached in " + str(niter) + "iterations")


def f(entrada):
    #return math.exp(x) - x - 1
    # return math.exp(x-2) - math.log(x-1) - x**2 + 4*x - 5
    # return math.exp(x) - x - 1
    0


def fd(entrada):
    #return math.exp(x) - 1
    # return -2*x + math.exp(x-2) - (1/x-1) + 4
    # return math.exp(x) - 1
    0


def d2f(x):
    return math.exp(x)
    # return math.exp(-2) + x
    # return 6*x + 2*math.cos(2*(x-1)) - 2
