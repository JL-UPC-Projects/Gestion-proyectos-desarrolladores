"""Presupuesto: control financiero del proyecto contra el costo ejecutado."""
from servicios.validaciones import numero


class Presupuesto:
    """Consolida el costo ejecutado y expone el saldo restante.

    ``actualizar_ejecucion`` recibe el **total** consolidado; no acumula
    nuevamente para evitar duplicar importes al consultar varias veces.
    """

    def __init__(self, monto_total):
        self.monto_total = numero(monto_total)
        self.monto_ejecutado = 0.0

    def actualizar_ejecucion(self, costo):
        # Recibe el total consolidado; no vuelve a sumar importes anteriores.
        self.monto_ejecutado = numero(costo, permitir_cero=True)

    def calcular_saldo(self):
        return self.monto_total - self.monto_ejecutado

    def verificar_exceso(self):
        return self.calcular_saldo() < 0