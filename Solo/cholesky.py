#!/usr/bin/python3

from math import sqrt
from pprint import pprint

tablaA = []

def cholesky(A):
    L = [[0.0] * len(A) for _ in range(len(A))]
    for i, (Ai, Li) in enumerate(zip(A, L)):
        for j, Lj in enumerate(L[:i+1]):
            s = sum(Li[k] * Lj[k] for k in range(j))
            Li[j] = sqrt(Ai[i] - s) if (i == j) else \
                      (1.0 / Lj[j] * (Ai[j] - s))
    return L
 
a11 = float(input('Ingresa el valor a11: '))
a12 = float(input('Ingresa el valor a12: '))
a13 = float(input('Ingresa el valor a13: '))
a21 = float(input('Ingresa el valor a21: '))
a22 = float(input('Ingresa el valor a22: '))
a23 = float(input('Ingresa el valor a23: '))
a31 = float(input('Ingresa el valor a31: '))
a32 = float(input('Ingresa el valor a32: '))
a33 = float(input('Ingresa el valor a33: '))

tablaA.append([a11,a12,a13])
tablaA.append([a21,a22,a23])
tablaA.append([a31,a32,a33])
L = cholesky(tablaA)

print("A:")
pprint(tablaA)

print("L:")
pprint(L)