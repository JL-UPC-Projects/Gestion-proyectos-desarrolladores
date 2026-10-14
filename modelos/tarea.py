"""Tarea: unidad de trabajo dentro de un proyecto con un responsable."""
from servicios.constantes import ESTADOS_TAREA
from servicios.validaciones import texto


class Tarea:
    """Sólo tres estados válidos: ``Pendiente``, ``En proceso`` y
    ``Finalizada``. La unicidad del código se verifica dentro del proyecto
    al ejecutar ``registrar_tarea``.
    """

    def __init__(self, codigo, titulo, proyecto, responsable):
        self.codigo = texto(codigo)
        self.titulo = texto(titulo)
        self.proyecto = proyecto
        self.estado = ESTADOS_TAREA[0]  # 'Pendiente'
        self.registros = []
        self.asignar_responsable(responsable)

    def registrar_tarea(self):
        if any(t.codigo == self.codigo for t in self.proyecto.tareas):
            raise ValueError('Código de tarea duplicado en el proyecto.')
        self.proyecto.tareas.append(self)

    def asignar_responsable(self, empleado):
        if empleado not in self.proyecto.consultar_personal_asignado():
            raise ValueError('El responsable debe estar asignado al proyecto.')
        self.responsable = empleado

    def actualizar_estado(self, estado):
        if estado not in ESTADOS_TAREA:
            raise ValueError(f'Estado de tarea inválido. Use uno de {ESTADOS_TAREA}.')
        self.estado = estado