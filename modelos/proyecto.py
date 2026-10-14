"""Proyecto: agrupa tareas y asignaciones contra un cliente y presupuesto."""
from servicios.constantes import ESTADOS_PROYECTO
from servicios.validaciones import texto


class Proyecto:
    """Mantiene listas de referencias compartidas (no copias) para que las
    consultas de avance y personal asignado reflejen el último estado.
    """

    ESTADO_INICIAL = ESTADOS_PROYECTO[0]  # 'Planificado'

    def __init__(self, codigo, nombre, cliente, presupuesto):
        self.codigo = texto(codigo)
        self.nombre = texto(nombre)
        self.cliente = cliente
        self.presupuesto = presupuesto
        self.estado = self.ESTADO_INICIAL
        self.asignaciones = []
        self.tareas = []

    def registrar_proyecto(self):
        """El alta la gestiona ``GestorDatos``; mantenemos el método para
        no romper el contrato declarado en el UML."""
        raise NotImplementedError('Registrar mediante GestorDatos.registrar_proyecto().')

    def consultar_personal_asignado(self):
        """Devuelve los empleados únicos con asignación activa en el proyecto."""
        return list({a.empleado.codigo: a.empleado for a in self.asignaciones
                     if a.estado == 'Activa'}.values())

    def calcular_avance(self):
        """Porcentaje (0–100) de tareas finalizadas sobre el total."""
        if not self.tareas:
            return 0.0
        return 100 * sum(t.estado == 'Finalizada' for t in self.tareas) / len(self.tareas)