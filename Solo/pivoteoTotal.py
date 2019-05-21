def linearsolver(A,k,n):
    # A = [[-1,0,0,4,-1,0],[0,-1,0,-1,4,-1],[4,-1,0,-1,-1,0],[-1,5,-1,0,-1,0],[0,-1,5,0,0,-1],[0,0,-1,0,-1,6]]
    # b = [61,14,8,5,9,23]

    

    mayor = 0
    filaMayor = k
    columnaMayor = k
    
    marcas = [0 for i in range(n)]
    for i in range(1,n+1):
        marcas[i-1] = i
    for i in range(k,n):
        for j in range(k,n):
            if(abs(A[i][j]) > mayor):
                mayor = abs(A[i][j])
                filaMayor = i
                columnaMayor = j
            else:
                pass
    if mayor == 0:
        print("El sistema no tiene solucion unica")
    else:
        if filaMayor != k:
            A = swapRows(A,filaMayor,k)
        if columnaMayor != k:
            A = swapCols(A,columnaMayor,k)
            temp = marcas[columnaMayor]
            marcas[columnaMayor] = marcas[k]
            marcas[k] = temp
    print("marcas:",marcas)
    return A

def swapRows(A,rowA,rowB):
    tmpRow = A[rowA]
    A[rowA] = A[rowB]
    A[rowB] = tmpRow
    return A

def swapCols(A,colA,colB):
    for i in range(len(A)):
        temp = A[i][colA]
        A[i][colA] = A[i][colB]
        A[i][colB] = temp
    return A

def main():
    #A = [[1,1,1,1],[27,9,3,1],[27,9,3,1],[125,25,5,1]]
    #b = [10,24,24,7]
    # A = [[-1,0,0,4,-1,0],[0,-1,0,-1,4,-1],[4,-1,0,-1,-1,0],[-1,5,-1,0,-1,0],[0,-1,5,0,0,-1],[0,0,-1,0,-1,6]]
    # b = [61,14,8,5,9,23]
    #A = [[2,-1,1],[3,3,7],[3,3,5]]
    #b = [-1,0,4]
    #A = [[0,2,3,5],[1,2,-5,7],[2,-4,0,3],[5,9,3,-3]]
    #b = [10,5,-1,14]
    A = [[1,1,1,1],[3.375,2.25,1.5,1],[3.375,2.25,1.5,1],[8,4,2,1]]
    b = [2.4,5.625,5.625,10.6]
    i = 0
    for x in A:
        x.append(b[i])
        i += 1
    n = len(A)

    for k in range(0,n-1):
        print("iteracion: ",k)
        A = linearsolver(A,k,n)
        for i in range(k+1,n):
            mult = A[i][k] / A[k][k]
            for j in range(k,n+1):
                A[i][j] = A[i][j] - mult * A[k][j]
        print("A: ", A)
    
    x = [0 for i in range(n)]

    x[n-1] =float(A[n-1][n])/A[n-1][n-1]
    for i in reversed(range(0,n)):
        z = 0
        for j in range(i+1,n):
            z = z  + float(A[i][j])*x[j]
        x[i] = float(A[i][n] - z)/A[i][i]
        print("x",i,": ",x[i])

if __name__ == "__main__":
    main()