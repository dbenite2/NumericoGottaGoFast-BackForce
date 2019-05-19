#!/usr/bin/python3

import numpy as np

# A = [[2,-1,1],[3,3,7],[3,3,5]]
# B = []

# rows = int(input("Ingresa el tamaño de la matriz a: "))
# # print("Ingresa la matriz A %s x %s: "% (rows, rows))
# # for i in range(rows):
# #     A.append(list(map(float, input().rstrip().split())))

# print("Ingresa la matriz B 1 x %s: "% (rows))
# for i in range(rows):
#     B.append(list(map(float, input().rstrip().split())))

# print(B)


# # Matriz aumentada
# AB = np.concatenate((A,B), axis=1)
# print('matriz aumentada:')
# print(AB)

# tamano = np.shape(AB)
# n = tamano[0]
# m = [[0 for i in range(len(B))]]
# print (m)
# size = np.shape(m)
# #m = tamano[1]
# x = [0 for i in range(len(B))]

# if n == size[1]:
#     for k in range(n):
#         mayor = 0
#         filam = k
#         for p in range(k,n):
#             if(mayor < abs(AB[p][k])):
#                 mayor = abs(AB[p][k])
#                 filam = p
#         if mayor == 0:
#             print("infinitas soluciones")
#             break
#         elif filam != k:
#             for j in range(n+1):
#                 aux = AB[k][j]
#                 AB[k][j] = AB[filam][j]
#                 AB[filam][j] = aux
#         for i in range(k,n-1):
#             loco = AB[i][k] / AB[k][k]
#             m[i][k] = loco
#             for j in range(k,n+1):
#                 AB[i][j] = AB[i][j] - (m[i][k]*AB[k][j])
#     for i in reversed(range(n-1)):
#         suma = 0
#         for p in range(i,n):
#             suma += AB[i][i] * x[p]
#         x[i] = (B[i][0] - suma)/AB[i][i]
# else :
#     print("matriz no cuadrada")


# # SALIDA
# print('aumentada: ')
# print(AB)
# print('X: ')
# print(x)


def linearsolver():
    A = [[-1,0,0,4,-1,0],[0,-1,0,-1,4,-1],[4,-1,0,-1,-1,0],[-1,5,-1,0,-1,0],[0,-1,5,0,0,-1],[0,0,-1,0,-1,6]]
    b = [61,14,8,5,9,23]
    
    n = len(A)
    M = A

    i = 0
    for x in M:
        x.append(b[i])
        i += 1
    
    print(M)

    for k in range(n):
        print("iteracion ",k)
        for i in range(k,n):
            if abs(M[i][k]) > abs(M[k][k]):
                M[k], M[i] = M[i],M[k]
            else:
                pass

        for j in range(k+1,n):
            q = float(M[j][k]) / M[k][k]
            for m in range(k, n+1):
                M[j][m] -=  q * M[k][m]
        
        #print de analisis
        print(M) 

    x = [0 for i in range(n)]

    x[n-1] =float(M[n-1][n])/M[n-1][n-1]
    for i in range (n-1,-1,-1):
        z = 0
        for j in range(i+1,n):
            z = z  + float(M[i][j])*x[j]
        x[i] = float(M[i][n] - z)/M[i][i]
        print("x",i,": ",x[i])

def main():
    linearsolver()

if __name__ == "__main__":
    main()


