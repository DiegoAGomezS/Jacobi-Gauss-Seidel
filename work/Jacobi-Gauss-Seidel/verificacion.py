from math import isfinite

TOLERANCIA = 1e-9


def verificar_matriz(matriz):
    if not isinstance(matriz, (list, tuple)) or not matriz:
        return False
    if not all(isinstance(fila, (list, tuple)) and fila for fila in matriz):
        return False
    columnas = len(matriz[0])
    if any(len(fila) != columnas for fila in matriz):
        return False
    try:
        return all(isfinite(float(valor)) for fila in matriz for valor in fila)
    except (TypeError, ValueError, OverflowError):
        return False


def verificar_vector(vector):
    if not isinstance(vector, (list, tuple)) or not vector:
        return False
    try:
        return all(isfinite(float(valor)) for valor in vector)
    except (TypeError, ValueError, OverflowError):
        return False


def obtener_dimensiones_matriz(matriz):
    if not verificar_matriz(matriz):
        raise ValueError("La matriz no es válida.")
    return len(matriz), len(matriz[0])


def verificar_matriz_cuadrada(matriz):
    if not verificar_matriz(matriz):
        return False
    filas, columnas = obtener_dimensiones_matriz(matriz)
    return filas == columnas


def verificar_vector_independiente(matriz, vector_b):
    if not verificar_matriz_cuadrada(matriz) or not verificar_vector(vector_b):
        return False
    return len(vector_b) == len(matriz)


def verificar_vector_inicial(matriz, vector_inicial):
    if not verificar_matriz_cuadrada(matriz) or not verificar_vector(vector_inicial):
        return False
    return len(vector_inicial) == len(matriz)


def verificar_dimensiones_sistema(matriz, vector_b, vector_inicial):
    return (
        verificar_matriz_cuadrada(matriz)
        and verificar_vector_independiente(matriz, vector_b)
        and verificar_vector_inicial(matriz, vector_inicial)
    )


def verificar_diagonal_no_nula(matriz):
    if not verificar_matriz_cuadrada(matriz):
        return False
    return all(matriz[i][i] != 0 for i in range(len(matriz)))


def verificar_diagonal_dominante(matriz, estricta=False):
    if not verificar_matriz_cuadrada(matriz):
        return False

    for i in range(len(matriz)):
        diagonal = abs(matriz[i][i])
        suma_restante = sum(
            abs(matriz[i][j])
            for j in range(len(matriz))
            if j != i
        )

        if estricta:
            if diagonal <= suma_restante:
                return False
        elif diagonal < suma_restante:
            return False

    return True


def verificar_convergencia(error, tolerancia):
    try:
        error = float(error)
        tolerancia = float(tolerancia)
        return (
            isfinite(error)
            and isfinite(tolerancia)
            and error >= 0
            and tolerancia > 0
            and error <= tolerancia
        )
    except (TypeError, ValueError, OverflowError):
        return False


def calcular_residuo(matriz, vector_x, vector_b):
    if not verificar_dimensiones_sistema(matriz, vector_b, vector_x):
        raise ValueError("Las dimensiones del sistema no son válidas.")

    residuo = []

    for i in range(len(matriz)):
        resultado = sum(
            matriz[i][j] * vector_x[j]
            for j in range(len(matriz))
        )
        residuo.append(resultado - vector_b[i])

    return max(abs(valor) for valor in residuo)


def verificar_residuo(matriz, vector_x, vector_b, tolerancia=TOLERANCIA):
    try:
        tolerancia = float(tolerancia)
        if not isfinite(tolerancia) or tolerancia <= 0:
            return False
        residuo = calcular_residuo(matriz, vector_x, vector_b)
        return residuo <= tolerancia
    except (TypeError, ValueError, OverflowError):
        return False