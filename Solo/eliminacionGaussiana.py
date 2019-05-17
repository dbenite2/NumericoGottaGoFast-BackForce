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

print(' *** Gauss elimina hacia adelante ***')
casicero = 0
# Gauss elimina hacia adelante
tamano = np.shape(AB)
n = tamano[0]
m = tamano[1]
for i in range(0,n,1):
    print("Entré")
    pivote = AB[i,i]
    adelante = i+1 
    for k in range(adelante,n,1):
        if (np.abs(AB[k,i])>=casicero):
            coeficiente = pivote/AB[k,i]
            AB[k,:] = AB[k,:]*coeficiente - AB[i,:]
        else:
            coeficiente= 'division para cero'
        print('coeficiente: ',coeficiente)
        print(AB)

print(' *** Gauss-Jordan elimina hacia atras *** ')
# Gauss-Jordan elimina hacia atras
ultfila = n-1
ultcolumna = m-1
for i in range(ultfila,0-1,-1):
    # Normaliza a 1 elemento diagonal
    AB[i,:] = AB[i,:]/AB[i,i]
    pivote = AB[i,i] # uno
    # arriba de la fila i
    atras = i-1 
    for k in range(atras,0-1,-1):
        if (np.abs(AB[k,i])>=casicero):
            coeficiente = pivote/AB[k,i]
            AB[k,:] = AB[k,:]*coeficiente - AB[i,:]
        else:
            coeficiente= 'division para cero'
        print('coeficiente: ', coeficiente)
        print(AB)
X = AB[:,ultcolumna]
X = np.transpose([X])

# SALIDA
print('aumentada: ')
print(AB)
print('X: ')
print(X)