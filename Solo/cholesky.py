#!/usr/bin/python3

from math import sqrt
from pprint import pprint

tablaA = []

def cholesky(A):
    L = [[0.0] * len(A) for _ in range(len(A))]
    for i, (Ai, Li) in enumerate(zip(A, L)):
        for j, Lj in enumerate(L[:i+1]):
            s = sum(Li[k] * Lj[k] for k in range(j))
            Li[j] = sqrt(Ai[i] - s) if (i == j) else (1.0 / Lj[j] * (Ai[j] - s))
    return L
 
rows = int(input("Ingresa el tamaño de la matriz: "))
print("Ingresa la matriz %s x %s: "% (rows, rows))
for i in range(rows):
    tablaA.append(list(map(int, input().rstrip().split())))

L = cholesky(tablaA)

print("A:")
pprint(tablaA)

print("L:")
pprint(L)