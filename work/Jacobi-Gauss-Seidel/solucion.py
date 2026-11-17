from . import verificacion as ver
from . import operaciones as op


def resolver_jacobi(matriz, vector_b, vector_inicial, tolerancia=1e-6, max_iteraciones=100):
    if not ver.verificar_dimensiones_sistema(matriz, vector_b, vector_inicial):
        raise ValueError("Las dimensiones del sistema no son válidas.")

    if not ver.verificar_diagonal_no_nula(matriz):
        raise ValueError("La diagonal principal contiene valores iguales a cero.")

    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")

    if max_iteraciones <= 0:
        raise ValueError("El máximo de iteraciones debe ser mayor que cero.")

    vector_actual = vector_inicial.copy()
    historial = []
    convergio = False

    for iteracion in range(1, max_iteraciones + 1):
        vector_nuevo = op.calcular_iteracion_jacobi(
            matriz,
            vector_b,
            vector_actual
        )

        error = op.calcular_error_anterior(vector_nuevo, vector_actual)
        residuo = op.calcular_residuo(matriz, vector_nuevo, vector_b)

        historial.append({
            "iteracion": iteracion,
            "valores": vector_nuevo.copy(),
            "error": error,
            "residuo": residuo
        })

        vector_actual = vector_nuevo

        if ver.verificar_convergencia(error, tolerancia):
            convergio = True
            break

    return {
        "metodo": "Jacobi",
        "solucion": vector_actual,
        "iteraciones": len(historial),
        "error": historial[-1]["error"] if historial else None,
        "residuo": historial[-1]["residuo"] if historial else None,
        "convergio": convergio,
        "historial": historial
    }


def resolver_gauss_seidel(matriz, vector_b, vector_inicial, tolerancia=1e-6, max_iteraciones=100):
    if not ver.verificar_dimensiones_sistema(matriz, vector_b, vector_inicial):
        raise ValueError("Las dimensiones del sistema no son válidas.")

    if not ver.verificar_diagonal_no_nula(matriz):
        raise ValueError("La diagonal principal contiene valores iguales a cero.")

    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")

    if max_iteraciones <= 0:
        raise ValueError("El máximo de iteraciones debe ser mayor que cero.")

    vector_actual = vector_inicial.copy()
    historial = []
    convergio = False

    for iteracion in range(1, max_iteraciones + 1):
        vector_nuevo = op.calcular_iteracion_gauss_seidel(
            matriz,
            vector_b,
            vector_actual
        )

        error = op.calcular_error_anterior(vector_nuevo, vector_actual)
        residuo = op.calcular_residuo(matriz, vector_nuevo, vector_b)

        historial.append({
            "iteracion": iteracion,
            "valores": vector_nuevo.copy(),
            "error": error,
            "residuo": residuo
        })

        vector_actual = vector_nuevo

        if ver.verificar_convergencia(error, tolerancia):
            convergio = True
            break

    return {
        "metodo": "Gauss-Seidel",
        "solucion": vector_actual,
        "iteraciones": len(historial),
        "error": historial[-1]["error"] if historial else None,
        "residuo": historial[-1]["residuo"] if historial else None,
        "convergio": convergio,
        "historial": historial
    }