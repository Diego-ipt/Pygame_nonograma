def procesar_fila_o_columna(linea):
    resultado = []
    contador = 0

    for valor in linea:
        if valor == 1:
            contador += 1
        else:
            if contador > 0:
                resultado.append(contador)
            contador = 0

    if contador > 0:
        resultado.append(contador)
    
    return tuple(resultado)

def procesar_matriz(matriz):
    N = len(matriz)

    # Procesar filas
    filas_resultado = []
    for fila in matriz:
        filas_resultado.append(procesar_fila_o_columna(fila))

    # Procesar columnas
    columnas_resultado = []
    for col in range(N):
        columna = [matriz[fila][col] for fila in range(N)]
        columnas_resultado.append(procesar_fila_o_columna(columna))

    return filas_resultado, columnas_resultado

# # Ejemplo
# matriz=[[1, 0, 1, 1, 0],
#         [0, 1, 0, 0, 1],
#         [1, 1, 1, 0, 0],
#         [0, 0, 1, 1, 1],
#         [1, 0, 0, 1, 0]]



# filas, columnas = procesar_matriz(matriz)
# print("Filas:", filas)
# print("Columnas:", columnas)

