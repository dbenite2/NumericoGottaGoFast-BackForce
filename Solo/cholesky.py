#!/usr/bin/python3

from math import sqrt
from pprint import pprint

tablaA = []
 
def cholesky(C):
    
    m = len(C)

    L = [[0.0] * m for i in range(m)]

    for i in range(m):
        for j in range(i+1):
            Temp = sum(L[i][k] * L[j][k] for k in range(j))
            
		# For Diagonal elements
            if (i == j):
                
                L[i][j] = sqrt(C[i][i] - Temp)
            else:
                # For Non Diagonal Elements
                L[i][j] = (1.0 / L[j][j] * (C[i][j] - Temp))
    return L
 
rows = int(input("Ingresa el tamaño de la fila: "))
colum = int(input("Ingresa el tamaño de la columna: "))
print("Ingresa la matriz: ")
print("Ejemplo: ")
print("2 5 18 8")
print("5 18 46")
print("18 46 327")
for i in range(rows):
    tablaA.append(list(map(int, input().rstrip().split())))

L = cholesky(tablaA)

print("A:")
pprint(tablaA)

print("L:")
pprint(L)