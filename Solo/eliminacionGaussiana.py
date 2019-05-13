#!/usr/bin/python3
import numpy as np

tablaA = []
tablaB = []

def eliminacion_gaussiana_pivoteo(A,b,metodo):
    n = len(A)
    marcas = np.arange(n)
    Ab = forma_matriz_aumentada(A,b,n)
    for k in range(n-1):
        print ("Etapa ",k)
        if metodo == 1:
            Ab = pivoteo_parcial(Ab,k,n)
        elif metodo == 2:
            Ab,marcas = pivoteo_total(Ab,k,marcas,n)
            print ("Marcas ",marcas)
        elif metodo == 3:
            s = []
            for i in range(len(A)):
                s.append(max(A[i]))
            print(s)
            Ab = pivoteo_escalonado(Ab,k,n,s)
        for i in range(k+1,n):
            if Ab[k][k]:
                multiplicador = Ab[i][k]/float(Ab[k][k])
                print ("multiplicador fila ",i," ",multiplicador)
            else:
                # raise Exception("Error, división por 0")
                sys.exit()
                print ("Error, división por 0")
            for j in range(k,n+1):
                Ab[i][j] = Ab[i][j] - multiplicador * Ab[k][j]

        print ("Matriz aumentada \n",npy.array(Ab))

    if metodo ==  1:
        return Ab
    elif metodo == 2:
        return Ab,marcas

def forma_matriz_aumentada(A,b,n):
    for i in range(n):
        A[i].append(b[i])
    return A

def sustitucion_regresiva(Ab):
    n = len(Ab)
    x= npy.zeros(n)
    for i in range(n-1,-1,-1):
        sumatoria = 0
        for p in range(i+1,n):
            sumatoria += Ab[i][p]*x[p]
        x[i] = (Ab[i][n]-sumatoria)/float(Ab[i][i])
    return x

def pivoteo_parcial(Ab,k,n):
    mayor =  abs(Ab[k][k])
    fila_mayor = k

    for s in range(k+1,n):
        if abs(Ab[s][k]) > mayor:
            mayor = abs(Ab[s][k])
            fila_mayor = s

    if mayor == 0:
        return "El sistema no tiene solucion unica"
    else:
        if fila_mayor != k:
            Ab = IntercambieFilas(Ab,fila_mayor,k)
        return Ab

# fila k = fila_mayor fila_mayor = k
def IntercambieFilas(Ab,fila_mayor,k):
    Ab[k], Ab[fila_mayor] = Ab[fila_mayor], Ab[k]
    return Ab

def main():
    global tablaA

    s = int(input('Ingresa el metodo PivoteoParcial = 1, PivoteoTotal = 2, PivoteoEscalonado = 3: '))

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

    print(tablaA)

    b11 = float(input('Ingresa el valor b11: '))
    b12 = float(input('Ingresa el valor b12: '))
    b13 = float(input('Ingresa el valor b13: '))   

    tablaB.append(b11)
    tablaB.append(b12)
    tablaB.append(b13)

    print(tablaB)

    eliminacion_gaussiana_pivoteo(tablaA,tablaB,s)


if __name__ == "__main__":
    main()

