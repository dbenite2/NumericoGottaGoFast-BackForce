def Lagrange(x,y,val):
        n = len(x)
        aux = [0.0 for i in range(n)]
        acum = 0.0

        for i in range(n):
            prod = 1.0
            for j in range(n):
                if(j != i):
                    prod *= (val - x[j])/(x[i] - x[j])
            aux[i] = prod
            acum += (aux[i]*y[i])
            
        
        return acum