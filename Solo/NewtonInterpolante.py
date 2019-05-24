def NewtonInter(x,y,val):
        n = len(x)
        aux = [[0.0 for i in range(n)] for i in range(n)]
        prod = 1.0
        acum = 0.0

        for i in range(n):
            aux[i][0] = y[i]
            for j in range(1,i):
                aux[i][j] = (aux[i][j-1] - aux[i-1][j-1])/(x[i]- x[i-j])
            if(i>0):
                prod *= val - x[i-1]
            acum += aux[i][i] * prod
        
        return acum

