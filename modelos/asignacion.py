"""Asignación: vincula un empleado con un proyecto durante una semana."""
from datetime import date

from servicios.constantes import ESTADOS_ASIGNACION
from servicios.validaciones import numero, texto


class Asignacion:
    """La semana se identifica por el lunes ISO del periodo en ``YYYY-MM-DD``.

    Mantiene la regla de capacidad (≤48h/semana por empleado) y de unicidad
    (un mismo empleado no puede tener dos asignaciones activas en la misma
    semana para el mismo proyecto).
    """

    def __init__(self, empleado, proyecto, semana, horas_semanales, rol):
        # La semana se identifica por su lunes, en formato YYYY-MM-DD.
        inicio = date.fromisoformat(semana)
        if inicio.weekday() != 0:
            raise ValueError('La semana debe identificarse por la fecha de su lunes.')
        self.empleado = empleado
        self.proyecto = proyecto
        self.semana = inicio.isoformat()
        self.horas_semanales = numero(horas_semanales)
        self.rol = texto(rol)
        self.estado = ESTADOS_ASIGNACION[0]  # 'Pendiente'

    def validar_disponibilidad(self):
        return self.empleado.verificar_disponibilidad(self.horas_semanales, self.semana)

    def registrar_asignacion(self):
        if self.estado != 'Pendiente':
            raise ValueError('Esta asignación ya fue registrada.')
        if any(a.proyecto.codigo == self.proyecto.codigo and a.semana == self.semana
               and a.estado == 'Activa' for a in self.empleado._asignaciones):
            raise ValueError('Ya existe una asignación activa para ese proyecto y semana.')
        if not self.validar_disponibilidad():
            raise ValueError('La asignación supera las 48 horas semanales.')
        self.estado = 'Activa'
        self.empleado._asignaciones.append(self)
        self.proyecto.asignaciones.append(self)

    def modificar_horas(self, horas):
        horas = numero(horas)
        if self.estado != 'Activa':
            raise ValueError('La asignación no está activa.')
        if horas > self.empleado.horas_disponibles(self.semana) + self.horas_semanales:
            raise ValueError('La asignación supera las 48 horas semanales.')
        self.horas_semanales = horas

    def finalizar_asignacion(self):
        self.estado = 'Finalizada'