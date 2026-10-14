"""Reporte: genera listados en formato texto a partir del gestor de datos."""
from datetime import date

from modelos.calculadora_costos import CalculadoraCostos


class Reporte:
    """Genera listados en texto; ``fecha_emision`` opcional (útil para tests)."""

    def __init__(self, gestor, fecha_emision=None):
        self.gestor = gestor
        self.fecha_emision = fecha_emision or date.today().isoformat()

    def generar_reporte_proyectos(self):
        return [f'{p.codigo} | {p.nombre} | {p.estado}' for p in self.gestor.proyectos]

    def generar_reporte_empleados(self):
        return [f'{e.codigo} | {e.nombre} | {type(e).__name__}' for e in self.gestor.empleados]

    def generar_reporte_tareas(self):
        return [f'{t.codigo} | {t.titulo} | {t.estado}'
                for proyecto in self.gestor.proyectos for t in proyecto.tareas]

    def generar_reporte_costos(self):
        return [f'{p.codigo} | saldo: S/ {CalculadoraCostos.calcular_saldo(p):.2f}'
                for p in self.gestor.proyectos]