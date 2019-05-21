def Lagrange(x,y,val):
        n = len(x)
        l = [0.0 for i in range(n)]
        acum = 0.0
        valorfx = 0

        for i in range(n):
            prod = 1.0
            for j in range(n):
                if(j != i):
                    prod *= (val - x[j])/(x[i] - x[j])
            l[i] = prod
            valorfx = (l[i]*y[i]) 
            acum += (l[i]*y[i])
            print ("L",i," f(x",i,"): ",l[i]," ", valorfx)
            
        print("acum: ", acum)
        return acum

def main():
    x = [2, 2.2, 2.4, 2.6, 2.8, 3]
    y = [-8.721968, -11.390940, -14.345230, -17.583432, -21.104092, -24.905700]
    val = 2.45
    Lagrange(x,y,val)

if __name__ == "__main__":
    main()