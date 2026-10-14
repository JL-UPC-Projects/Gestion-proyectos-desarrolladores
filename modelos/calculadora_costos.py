"""CalculadoraCostos: agrega importes de registros contra el presupuesto."""


class CalculadoraCostos:
    """Servicios estáticos que consolidan costos y verifican presupuesto."""

    @staticmethod
    def calcular_costo_proyecto(proyecto):
        costo = sum(registro.calcular_importe()
                    for tarea in proyecto.tareas
                    for registro in tarea.registros)
        proyecto.presupuesto.actualizar_ejecucion(costo)
        return costo

    @staticmethod
    def calcular_saldo(proyecto):
        CalculadoraCostos.calcular_costo_proyecto(proyecto)
        return proyecto.presupuesto.calcular_saldo()

    @staticmethod
    def comparar_presupuesto(proyecto):
        return CalculadoraCostos.calcular_saldo(proyecto) >= 0