#!/usr/bin/python3

tablaA = []

def doolittle(A,n, met):
    L,U = inicializa(n,met)
    for k in range(n):
        suma1 = 0
        for p in range(0,k):
            suma1 += L[k][p]*U[p][k]
        U[k][k] = A[k][k]-suma1
        for i in range(k+1,n):
            suma2 = 0
            for p in range(k):
                suma2 += L[i][p]*U[p][k]
            if U[k][k] == 0:
                break
            else: 
                L[i][k] = (A[i][k]-suma2)/float(U[k][k])
        for j in range(k+1,n):
            suma3 = 0
            for p in range(k):
                suma3 += L[k][p]*U[p][j]
            if L[k][k] == 0:
                break
            else: 
                U[k][j]= (A[k][j]-suma3)/float(L[k][k])
        #imprimir L  U y k etapa

    determinante = (L[0][0]*L[1][1]*L[2][2])*(U[0][0]*U[1][1]*U[2][2])

    print("Solucion")
    print(L)
    print(U)
    print("Determinante")
    print(determinante)
    return L,U

#Doolittle == 0, Crout == 1, Cholesky == 2
def inicializa(n,metodo):
    L , U = [] , []
    if metodo == 0:
        L = [[1 if j == i else 0 for j in range(n)] for i in range(n)]
        U = [[0 for j in range(n)] for i in range(n)]
    elif metodo == 1:
        L = [[0 for j in range(n)] for i in range(n)]
        U = [[1 if j == i else 0 for j in range(n)] for i in range(n)]
    print(L)
    print(U)
    return L , U

def main():
    global tablaA

    s = int(input('Ingresa el metodo Doolittle = 0, Court = 1 '))

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

    doolittle(tablaA,3, s)


if __name__ == "__main__":
    main()
