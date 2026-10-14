"""QA: empleado responsable de pruebas funcionales o automatizadas."""
from modelos.empleado import Empleado
from servicios.validaciones import numero, texto


class QA(Empleado):
    """Tarifa por hora propia; la lógica de registrar_prueba queda
    pendiente de definición con el equipo (se documenta explícitamente).
    """

    TARIFA_HORA = 50

    def __init__(self, codigo, nombre, tipo_prueba, herramienta):
        super().__init__(codigo, nombre)
        self.tipo_prueba = texto(tipo_prueba)
        self.herramienta = texto(herramienta)

    def calcular_costo(self, horas):
        return numero(horas) * self.TARIFA_HORA

    def registrar_prueba(self, tarea):
        """Pendiente de acordar con el equipo; se mantiene explícito."""
        raise NotImplementedError('Pendiente: definir resultados de pruebas con el equipo.')