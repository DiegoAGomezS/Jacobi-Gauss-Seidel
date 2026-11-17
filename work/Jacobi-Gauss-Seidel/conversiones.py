
from fractions import Fraction
import math


def convertir_a_decimal(entrada):
    try:
        entrada = str(entrada).strip().replace(",", ".")

        if not entrada:
            return None

        valor = float(Fraction(entrada))

        if not math.isfinite(valor):
            return None

        return valor

    except (ValueError, ZeroDivisionError, OverflowError):
        return None


def convertir_a_fraccion(valor):
    try:
        fraccion = Fraction(str(valor)).limit_denominator(10000)

        if fraccion.denominator == 1:
            return str(fraccion.numerator)

        return f"{fraccion.numerator}/{fraccion.denominator}"

    except (ValueError, TypeError, ZeroDivisionError, OverflowError):
        return None


def convertir_vector_a_fracciones(vector):
    return [
        convertir_a_fraccion(valor)
        for valor in vector
    ]


def convertir_matriz_a_fracciones(matriz):
    return [
        convertir_vector_a_fracciones(fila)
        for fila in matriz
    ]


def convertir_vectores_a_fracciones(vectores):
    return [
        convertir_vector_a_fracciones(vector)
        for vector in vectores
    ]
