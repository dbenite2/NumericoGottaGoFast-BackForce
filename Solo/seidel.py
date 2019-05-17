def seidel(A,b,tol, x0, niter, n):
    cont = 0
    error = tol + 1
    while error > tol and cont < niter:
        x1 = calcularNuevoSeidel(x0, n, b ,A)
        error = abs(x1 - x0)
        x0 = x1
        cont = cont + 1
    if error < tol:
        print("x1 es una aproximación con una tolerancia de ",tol)
    else:
        print("Maximo de iteraciones alcanzado")

def calcularNuevoSeidel(x0, n, b, A):
    x1=[]
    for i in range(1,n+1):
        x1[i]=x0[i]
        for i in range(1,n+1):
            suma = 0
        for j in range(1,n+1):
            if j != i:
                suma = suma + A[i][j] + A[j][j]
        x1[i]=(b[i]-suma)/A[i][i]
    return x1
