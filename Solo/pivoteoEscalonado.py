def pivoteo_escalonado(Ab,k, n, s):
    mayor = 0
    fila_mayor = k
    cocientes = []
    for i in range(k,n):
        cocientes.append(abs(Ab[i][k])/s[i])
    fila_mayor = max(range(len(cocientes)), key = lambda i: cocientes[i])
    mayor = cocientes[fila_mayor]
    if mayor == 0:
        print("El sistema no tiene solucion unica")
    elif fila_mayor != k:
        Ab[k], Ab[fila_mayor] = Ab[fila_mayor], Ab[k]
        s[k],s[fila_mayor] = s[fila_mayor],s[k]
    return Ab
