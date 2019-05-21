
import math

def jacobi(A, b, n, tol, x0, niter):
    cont = 0
    dispersion = tol + 1
    x1 = []
    while (dispersion > tol) and (cont < niter):
        x1 = calcularNuevoJacobi(x0, n, b, A)
        #Normalizar x1 y x0 
        dispersion = abs((normalizar(x1) - normalizar(x0))/normalizar(x1))
        x0 = x1
        cont = cont +  1
        print('{:30},{:30},{:30}'.format(str(cont),str(x1),dispersion))
    if dispersion < tol:
        print("x1:",x1," es una aproximacion con una tolerancia" ,tol)
    else:
        print("Fracaso en niter iteraciones")

def calcularNuevoJacobi(x0, n, b, A):
    x1=[0 for i in range(n)]
    for i in range(0,n):
        suma = 0.0
        for j in range(n):
            if j != i:
                suma += A[i][j] * x0[j]
        x1[i]=(b[i]-suma)/A[i][i]
    return x1

def normalizar(x0):
    cont = 0
    for i in range(len(x0)):
        cont += abs(x0[i]) * abs(x0[i])
    return math.sqrt(cont)

def main():
    A = [[9,2,-3],[-3,-8,4],[3,2,-7]]
    b = [27,-61,-21]
    n = 3
    tol = 5e-6
    x0 = [2,4,5]
    niter = 20
    jacobi(A,b,n,tol,x0,niter)

if __name__ == "__main__":
    main()