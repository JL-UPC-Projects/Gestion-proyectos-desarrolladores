"""Desarrollador: empleado cuyo costo se cobra por horas a tarifa fija."""
from modelos.empleado import Empleado
from servicios.validaciones import numero, texto


class Desarrollador(Empleado):
    """Tarifa por hora definida a nivel de clase; basta consultar la
    subclase para conocerla sin necesidad de instanciar.
    """

    TARIFA_HORA = 60

    def __init__(self, codigo, nombre, lenguaje_principal, nivel):
        super().__init__(codigo, nombre)
        self.lenguaje_principal = texto(lenguaje_principal)
        self.nivel = texto(nivel)

    def calcular_costo(self, horas):
        return numero(horas) * self.TARIFA_HORA

    def aceptar_tarea(self, tarea):
        """Delega en la tarea para registrar el vínculo con el responsable."""
        tarea.asignar_responsable(self)