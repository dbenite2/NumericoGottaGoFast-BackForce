#!/usr/bin/python3

import numpy as np

A = []
B = []

rows = int(input("Ingresa el tamaño de la matriz a: "))
print("Ingresa la matriz A %s x %s: "% (rows, rows))
for i in range(rows):
    A.append(list(map(float, input().rstrip().split())))

print("Ingresa la matriz B 1 x %s: "% (rows))
for i in range(rows):
    B.append(list(map(float, input().rstrip().split())))



# Matriz aumentada
AB = np.concatenate((A,B), axis=1)
print('matriz aumentada:')
print(AB)

tamano = np.shape(AB)
n = tamano[0]
m = [[0 for i in range(len(B))]for i in range(len(B))]
size = np.shape(m)
#m = tamano[1]
x = [0 for i in range(len(B))]

if n == size[1]:
    for k in range(n):
        mayor = 0
        filam = k
        for p in range(k,n):
            if(mayor < abs(AB[p][k])):
                mayor = abs(AB[p][k])
                filam = p
        if mayor == 0:
            print("infinitas soluciones")
            break
        elif filam != k:
            for j in range(n):
                aux = AB[k][j]
                AB[k][j] = AB[filam][j]
                AB[filam][j] = aux
        for i in range(k+1,n):
            m[i][k] = AB[i][k] / AB[k][k]
            for j in range(k,n+1):
                AB[i][j] = AB[i][j] - (m[i][k]*AB[k][j])
    for i in reversed(range(n)):
        suma = 0
        for p in range(i+1,n):
            suma += AB[i][i] * x[p]
        x[i] = (B[i][0] - suma)/AB[i][i]
else :
    print("matriz no cuadrada")


# SALIDA
print('aumentada: ')
print(AB)
print('X: ')
print(x)




