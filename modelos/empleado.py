"""Empleado: clase base del dominio con la lógica de capacidad semanal."""
from servicios.constantes import CAPACIDAD_SEMANAL
from servicios.validaciones import numero, texto


class Empleado:
    """Clase base para Desarrollador, QA y LiderTecnico.

    Mantiene la lista interna de asignaciones como referencia compartida
    (no copia), de modo que la disponibilidad se calcule contra los mismos
    objetos que persisten en ``Proyecto.asignaciones``.
    """

    def __init__(self, codigo, nombre):
        # ``__codigo`` y ``__nombre`` se privatizan con doble underscore para
        # forzar el acceso a través de las ``@property`` declaradas abajo.
        self.__codigo = texto(codigo)
        self.__nombre = texto(nombre)
        self.__capacidad_semanal = CAPACIDAD_SEMANAL
        # Referencias compartidas, necesarias para consultar disponibilidad.
        self._asignaciones = []

    # --- Propiedades públicas ---------------------------------------------
    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def capacidad_semanal(self):
        return self.__capacidad_semanal

    # --- Comportamiento polimórfico --------------------------------------
    def calcular_costo(self, horas):
        """Método polimórfico: cada subclase aplica su propio tarifario."""
        raise NotImplementedError('Utilice Desarrollador, QA o LiderTecnico.')

    def horas_disponibles(self, semana):
        """Capacidad restante en la semana sumando asignaciones activas."""
        comprometidas = sum(a.horas_semanales for a in self._asignaciones
                            if a.semana == semana and a.estado == 'Activa')
        return self.__capacidad_semanal - comprometidas

    def verificar_disponibilidad(self, horas, semana):
        """¿Caben ``horas`` dentro de la disponibilidad restante?"""
        return numero(horas) <= self.horas_disponibles(semana)