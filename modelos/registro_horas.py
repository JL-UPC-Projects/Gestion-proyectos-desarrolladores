"""RegistroHoras: horas efectivas imputadas por un empleado a una tarea."""
from datetime import date

from servicios.validaciones import numero


class RegistroHoras:
    """La fecha debe caer dentro de la semana ISO de una asignación activa
    del empleado al proyecto de la tarea; de lo contrario, no se imputa.
    """

    def __init__(self, tarea, empleado, fecha, horas):
        self.tarea = tarea
        self.empleado = empleado
        self.fecha = date.fromisoformat(fecha).isoformat()
        self.horas = numero(horas)

    def validar_registro(self):
        fecha = date.fromisoformat(self.fecha)
        return any(a.proyecto is self.tarea.proyecto and a.estado == 'Activa'
                   and 0 <= (fecha - date.fromisoformat(a.semana)).days < 7
                   for a in self.empleado._asignaciones)

    def registrar_horas(self):
        if self.tarea not in self.tarea.proyecto.tareas:
            raise ValueError('La tarea no está registrada.')
        if self in self.tarea.registros:
            raise ValueError('Registro ya agregado.')
        if not self.validar_registro():
            raise ValueError('El empleado debe tener asignación activa en esa semana.')
        self.tarea.registros.append(self)

    def calcular_importe(self):
        """El cálculo delega en el empleado: aplica polimorfismo de tarifa."""
        return self.empleado.calcular_costo(self.horas)