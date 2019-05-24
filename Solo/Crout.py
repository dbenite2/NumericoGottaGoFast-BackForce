tablaA = []

def progresiva(l,b):
    z = [ 0 for i in range(len(b))]
    z[0] = b[0]/l[0][0]
    for i in range(1,len(b)):
        sum = 0
        for j in range(0,i):
            sum += l[i][j] * z[j]
        z[i] = ((b[i] - sum)/l[i][i])  

    print("Z: ")
    for i in range(len(z)):
        print(z[i])
    
    return z

def regresiva(u,z):
    n = len(z)
    x = [0 for i in range(len(z))]
    x[n-1] = z[n-1]/u[n-1][n-1]

    for i in reversed(range(0,n-1)):
        sum = 0
        for j in range(i+1,n):
            sum += u[i][j] * x[j]
        x[i] = ((z[i] - sum)/u[i][i])
    
    print("X: ")
    for i in range(len(x)):
        print("x",i,": ", x[i])    

def crout(A,n,b):
    L,U = inicializa(n)
    determinante = 1

    for k in range(0,n):
        suma1 = 0.0
        for p in range(0,k):
            suma1 += (L[k][p] * U[p][k])
        L[k][k] = A[k][k] - suma1
        U[k][k] = 1
        for i in range (k+1,n):
            suma2 = 0.0
            for p in range (0,k):
                suma2 += (L[i][p] * U[p][k])
            if (L[k][k] != 0):
                L[i][k] = (A[i][k] - suma2)/U[k][k]
            else:
                print("El sistema puede no tener solucion")
        for j in range(k+1,n):
            suma3 = 0.0
            for p in range (0,k):
                suma3 += (L[k][p] * U[p][j])
            if(L[k][k] != 0):
                U[k][j] = (A[k][j]-suma3)/L[k][k]
            else:
                print("El sistema puede no tener solucion")

        print("L solucion")
        for i in range(len(L)):
            print(L[i])
        print("U solucion")
        for i in range(len(U)):
            print(U[i])

    z = progresiva(L,b)
    x = regresiva(U,z)
    return x

def inicializa(n):
   
    L = [[0.0 for j in range(n)] for i in range(n)]
    U = [[1.0 if j == i else 0.0 for j in range(n)] for i in range(n)]
    
    return L , U


def main():
    global tablaA

   

    rows = int(input("Ingresa el tamaño de la matriz: "))
    print("Ingresa la matriz %s x %s: "% (rows, rows))
    for i in range(rows):
        tablaA.append(list(map(int, input().rstrip().split())))

    print("Matriz inicial: ")
    for i in range(len(tablaA)):
        print(tablaA[i]) 

    b = input("Ingrese el arreglo de resultados: ").split()
    
    for i in range(len(b)):
        b[i] = float(b[i])

   
    crout(tablaA,rows,b)


if __name__ == "__main__":
    main()
