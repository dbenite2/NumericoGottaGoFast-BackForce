#!/usr/bin/python3

tablaA = []

def doolittle(A,n, met):
    L,U = inicializa(n,met)
    determinante = 1
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

    for i in range(n):
        determinante = determinante * L[i-1][i-1]

    print("Solucion")
    print(L)
    print(U)
    print("Determinante es: ", determinante)
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

    s = int(input("Ingresa el metodo a implementar 0 para Doolittle y 1 para Crout: "))

    rows = int(input("Ingresa el tamaño de la matriz: "))
    print("Ingresa la matriz %s x %s: "% (rows, rows))
    for i in range(rows):
        tablaA.append(list(map(int, input().rstrip().split())))

    print(tablaA)

    doolittle(tablaA,rows, s)


if __name__ == "__main__":
    main()
