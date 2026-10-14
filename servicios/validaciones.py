"""Validaciones básicas reutilizadas por las clases de modelo."""
from math import isfinite


def texto(valor):
    """Cadena obligatoria (recorta espacios; lanza ``ValueError`` si queda vacía)."""
    valor = str(valor).strip()
    if not valor:
        raise ValueError('El campo no puede estar vacío.')
    return valor


def numero(valor, permitir_cero=False):
    """Convierte a ``float`` y rechaza inválidos; ``permitir_cero=True`` admite el cero."""
    valor = float(valor)
    if not isfinite(valor) or valor < 0 or (valor == 0 and not permitir_cero):
        raise ValueError('Ingrese un número válido mayor que cero.')
    return valor


def entero_no_negativo(valor):
    """Valida que el valor sea un entero no negativo."""
    numero_valor = numero(valor, permitir_cero=True)
    if not numero_valor.is_integer():
        raise ValueError('La cantidad debe ser un número entero.')
    return int(numero_valor)
