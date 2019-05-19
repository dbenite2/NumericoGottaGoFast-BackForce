import math

def seidel(A,b,n, tol,x0, niter):
    cont = 0
    error = tol + 1
    while error > tol and cont < niter:
        x1 = calcularNuevoSeidel(x0, n, b ,A)
        error = abs((normalizar(x1) - normalizar(x0))/normalizar(x1))
        x0 = x1
        cont = cont + 1
        print('{:30},{:30},{:+.2e}'.format(str(cont),str(x1),error))
    if error < tol:
        print("x1:",x1," es una aproximacion con una tolerancia" ,tol)
    else:
        print("Maximo de iteraciones alcanzado")

def calcularNuevoSeidel(x0, n, b, A):
    x1=[0 for i in range(n)]
    for i in range(0,n):
        x1[i]=x0[i]
    for i in range(0,n):
        suma = 0.0
        for j in range(0,n):
            if j != i:
                suma +=  A[i][j] * x1[j]
        x1[i]=(b[i]-suma)/A[i][i]
    return x1


def normalizar(x0):
    cont = 0
    for i in range(len(x0)):
        cont += abs(x0[i]) * abs(x0[i])
    return math.sqrt(cont)

def main():
    A = [[13,-4,-5],[3,-7,2],[-4,5,-16]] #Sistema de ecuaciones
    b = [-23,5,34] #coeficientes independientes
    n = 3 #tamaño de la matriz
    tol = 5e-6 
    x0 = [-3.4549112874812056, -2.8058466873035033, -2.138099267912043] # valores iniciales
    niter = 20
    seidel(A,b,n,tol,x0,niter)

if __name__ == "__main__":
    main()
