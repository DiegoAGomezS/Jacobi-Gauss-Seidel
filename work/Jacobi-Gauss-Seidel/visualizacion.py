from . import conversiones as conv


def formatear_valor(valor, formato="decimal", decimales=6):
    if formato == "fraccion":
        return conv.convertir_a_fraccion(valor)
    return f"{valor:.{decimales}f}"


def formatear_vector(vector, formato="decimal", decimales=6):
    return [
        formatear_valor(valor, formato, decimales)
        for valor in vector
    ]


def mostrar_matriz(matriz, formato="decimal", decimales=6):
    return "\n".join(
        "[ " + "   ".join(
            formatear_valor(valor, formato, decimales)
            for valor in fila
        ) + " ]"
        for fila in matriz
    )


def mostrar_sistema(matriz, vector_b, formato="decimal", decimales=6):
    resultado = []

    for i, fila in enumerate(matriz):
        ecuacion = " + ".join(
            f"({formatear_valor(valor, formato, decimales)})x{i + 1}"
            for valor in fila
        )
        resultado.append(
            f"{ecuacion} = {formatear_valor(vector_b[i], formato, decimales)}"
        )

    return "\n".join(resultado)


def mostrar_iteracion(iteracion, formato="decimal", decimales=6):
    numero = iteracion["iteracion"]
    valores = iteracion["valores"]
    error = iteracion["error"]
    residuo = iteracion["residuo"]

    valores_texto = ", ".join(
        f"x{i + 1} = {formatear_valor(valor, formato, decimales)}"
        for i, valor in enumerate(valores)
    )

    return (
        f"Iteración {numero}\n"
        f"{valores_texto}\n"
        f"Error: {formatear_valor(error, formato, decimales)}\n"
        f"Residuo: {formatear_valor(residuo, formato, decimales)}\n"
    )


def mostrar_historial(historial, formato="decimal", decimales=6):
    if not historial:
        return "No hay iteraciones registradas."

    resultado = []

    for iteracion in historial:
        resultado.append(
            mostrar_iteracion(iteracion, formato, decimales)
        )

    return "\n".join(resultado)


def mostrar_resultado(resultado, formato="decimal", decimales=6):
    solucion = resultado["solucion"]
    metodo = resultado["metodo"]
    iteraciones = resultado["iteraciones"]
    error = resultado["error"]
    residuo = resultado["residuo"]
    convergio = resultado["convergio"]

    estado = "Convergencia alcanzada" if convergio else "No se alcanzó la convergencia"

    solucion_texto = "\n".join(
        f"x{i + 1} = {formatear_valor(valor, formato, decimales)}"
        for i, valor in enumerate(solucion)
    )

    return (
        f"MÉTODO: {metodo}\n"
        f"ESTADO: {estado}\n"
        f"ITERACIONES: {iteraciones}\n\n"
        f"SOLUCIÓN APROXIMADA:\n"
        f"{solucion_texto}\n\n"
        f"ERROR FINAL: {formatear_valor(error, formato, decimales)}\n"
        f"RESIDUO FINAL: {formatear_valor(residuo, formato, decimales)}"
    )


def mostrar_procedimiento(resultado, formato="decimal", decimales=6):
    encabezado = mostrar_resultado(resultado, formato, decimales)
    historial = mostrar_historial(
        resultado["historial"],
        formato,
        decimales
    )

    return (
        f"{encabezado}\n\n"
        f"{'=' * 50}\n"
        f"DESARROLLO DE LAS ITERACIONES\n"
        f"{'=' * 50}\n\n"
        f"{historial}"
    )