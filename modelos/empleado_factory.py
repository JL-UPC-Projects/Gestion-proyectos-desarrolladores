"""EmpleadoFactory: punto único para instanciar Desarrollador/QA/Líder.

Centraliza el despacho por tipo y mantiene los nombres válidos en un solo
lugar. Tipo inválido → ``EmpleadoFactoryError`` (``ValueError``) con un
mensaje claro y la lista admitida.
"""
from servicios.constantes import TIPOS_EMPLEADO
from modelos.desarrollador import Desarrollador
from modelos.qa import QA
from modelos.lider_tecnico import LiderTecnico


class EmpleadoFactoryError(ValueError):
    """Tipo de empleado desconocido o argumentos insuficientes."""


class EmpleadoFactory:
    """Factory Method que encapsula la decisión de subclase.

    ``datos`` debe ser una lista/tupla con los argumentos específicos de
    la subclase, en el orden declarado en el UML:
      - Desarrollador(lenguaje_principal, nivel)
      - QA(tipo_prueba, herramienta)
      - LiderTecnico(tecnologia_principal, equipo_a_cargo)
    """

    @staticmethod
    def crear_empleado(tipo, codigo, nombre, datos):
        if not isinstance(datos, (list, tuple)):
            raise EmpleadoFactoryError(
                'El parámetro "datos" debe ser una lista o tupla.')
        if len(datos) < 2:
            raise EmpleadoFactoryError(
                'Cada tipo de empleado requiere al menos 2 datos adicionales.')

        if tipo == 'Desarrollador':
            return Desarrollador(codigo, nombre, datos[0], datos[1])
        if tipo == 'QA':
            return QA(codigo, nombre, datos[0], datos[1])
        if tipo == 'LiderTecnico':
            return LiderTecnico(codigo, nombre, datos[0], datos[1])

        raise EmpleadoFactoryError(
            f'Tipo de empleado inválido: {tipo!r}. Use uno de {TIPOS_EMPLEADO}.')