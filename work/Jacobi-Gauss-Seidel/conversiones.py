import math
from . import verificacion as ver


def calcular_error_anterior(vector_actual, vector_anterior):
    if not ver.verificar_vector(vector_actual) or not ver.verificar_vector(vector_anterior):
        raise ValueError("Los vectores proporcionados no son válidos.")

    if len(vector_actual) != len(vector_anterior):
        raise ValueError("Los vectores deben tener la misma dimensión.")

    return max(
        abs(vector_actual[i] - vector_anterior[i])
        for i in range(len(vector_actual))
    )


def calcular_residuo(matriz, vector_x, vector_b):
    return ver.calcular_residuo(matriz, vector_x, vector_b)


def calcular_valor_jacobi(matriz, vector_b, vector_anterior, indice):
    if not ver.verificar_dimensiones_sistema(matriz, vector_b, vector_anterior):
        raise ValueError("Las dimensiones del sistema no son válidas.")

    if not ver.verificar_diagonal_no_nula(matriz):
        raise ValueError("La diagonal principal contiene valores iguales a cero.")

    suma = sum(
        matriz[indice][j] * vector_anterior[j]
        for j in range(len(matriz))
        if j != indice
    )

    return (vector_b[indice] - suma) / matriz[indice][indice]


def calcular_valor_gauss_seidel(matriz, vector_b, vector_actual, indice):
    if not ver.verificar_dimensiones_sistema(matriz, vector_b, vector_actual):
        raise ValueError("Las dimensiones del sistema no son válidas.")

    if not ver.verificar_diagonal_no_nula(matriz):
        raise ValueError("La diagonal principal contiene valores iguales a cero.")

    suma = sum(
        matriz[indice][j] * vector_actual[j]
        for j in range(len(matriz))
        if j != indice
    )

    return (vector_b[indice] - suma) / matriz[indice][indice]


def calcular_iteracion_jacobi(matriz, vector_b, vector_anterior):
    if not ver.verificar_dimensiones_sistema(matriz, vector_b, vector_anterior):
        raise ValueError("Las dimensiones del sistema no son válidas.")

    if not ver.verificar_diagonal_no_nula(matriz):
        raise ValueError("La diagonal principal contiene valores iguales a cero.")

    return [
        calcular_valor_jacobi(matriz, vector_b, vector_anterior, i)
        for i in range(len(matriz))
    ]


def calcular_iteracion_gauss_seidel(matriz, vector_b, vector_anterior):
    if not ver.verificar_dimensiones_sistema(matriz, vector_b, vector_anterior):
        raise ValueError("Las dimensiones del sistema no son válidas.")

    if not ver.verificar_diagonal_no_nula(matriz):
        raise ValueError("La diagonal principal contiene valores iguales a cero.")

    vector_actual = vector_anterior.copy()

    for i in range(len(matriz)):
        vector_actual[i] = calcular_valor_gauss_seidel(
            matriz,
            vector_b,
            vector_actual,
            i
        )

    return vector_actual


def calcular_norma_infinito(vector):
    if not ver.verificar_vector(vector):
        raise ValueError("El vector proporcionado no es válido.")

    return max(abs(valor) for valor in vector)


def verificar_valores_finitos(vector):
    return all(math.isfinite(float(valor)) for valor in vector)