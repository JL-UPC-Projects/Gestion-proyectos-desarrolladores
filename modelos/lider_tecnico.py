"""Líder técnico: empleado a cargo de un equipo y con tarifa premium."""
from modelos.empleado import Empleado
from servicios.validaciones import numero, texto


class LiderTecnico(Empleado):
    """Tarifa premium y responsabilidad adicional de revisar el avance del
    proyecto delegando en ``Proyecto.calcular_avance``.
    """

    TARIFA_HORA = 90

    def __init__(self, codigo, nombre, tecnologia_principal, equipo_a_cargo):
        super().__init__(codigo, nombre)
        self.tecnologia_principal = texto(tecnologia_principal)
        # ``equipo_a_cargo`` puede ser cero (líder sin equipo asignado) pero
        # nunca negativo ni no entero.
        valor = numero(equipo_a_cargo, permitir_cero=True)
        if not valor.is_integer():
            raise ValueError('La cantidad de integrantes debe ser entera.')
        self.equipo_a_cargo = int(valor)

    def calcular_costo(self, horas):
        return numero(horas) * self.TARIFA_HORA

    def revisar_avance(self, proyecto):
        return proyecto.calcular_avance()