def jacobi(A, b, n, tol, x0, niter):
    cont = 0
    dispersion = tol + 1
    x1 = []
    while (dispersion > tol) and (cont < niter):
        x1 = calcularNuevoJacobi(x0, n, b, A)
        dispersion = abs(x1 - x0)
        x0 = x1
        cont = cont +  1
    if dispersion < tol:
        print("x1 es una aproximacion con una tolerancia" ,tol)
    else:
        print("Fracaso en niter iteraciones")

def calcularNuevoJacobi(x0, n, b, A):
    x1=[]
    for i in range(1,n):
        suma = 0.0
        for j in range(n):
            if j != i:
                suma = suma + A[i][j] + x0[j]
        x1[i]=(b[i]-suma)/A[i][i]
    return x1
