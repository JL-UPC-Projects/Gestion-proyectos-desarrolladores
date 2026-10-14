"""Pruebas para registrar empleados (casos 1, 2) y validar tarifas (caso 8)."""
import unittest

from modelos.empleado_factory import EmpleadoFactory, EmpleadoFactoryError
from modelos.gestor_datos import GestorDatos


class EmpleadoTests(unittest.TestCase):
    """Cubre la creación de las tres subclases, el rechazo por código
    duplicado y la verificación del tarifario polimórfico.
    """

    def setUp(self):
        self.gestor = GestorDatos()

    # --- Caso 1: registrar empleado válido (Desarrollador/QA/LiderTecnico)
    def test_registrar_desarrollador_qa_lider_via_factory(self):
        """Crear las tres subclases con ``EmpleadoFactory`` y confirmar
        que el gestor las conserva con sus tipos y atributos propios.
        """
        dev = EmpleadoFactory.crear_empleado(
            'Desarrollador', 'E001', 'Ana', ['Python', 'Junior'])
        qa = EmpleadoFactory.crear_empleado(
            'QA', 'E002', 'Luis', ['Funcional', 'Manual'])
        lider = EmpleadoFactory.crear_empleado(
            'LiderTecnico', 'E003', 'Marta', ['Python', 2])

        self.gestor.registrar_empleado(dev)
        self.gestor.registrar_empleado(qa)
        self.gestor.registrar_empleado(lider)

        self.assertEqual(len(self.gestor.empleados), 3)
        self.assertIs(self.gestor.buscar_empleado('E001'), dev)
        self.assertIs(self.gestor.buscar_empleado('E002'), qa)
        self.assertIs(self.gestor.buscar_empleado('E003'), lider)
        self.assertEqual(dev.lenguaje_principal, 'Python')
        self.assertEqual(qa.herramienta, 'Manual')
        self.assertEqual(lider.equipo_a_cargo, 2)

    def test_factory_rechaza_tipo_invalido(self):
        """Tipo desconocido debe lanzar ``EmpleadoFactoryError`` (que es
        ``ValueError``) y no corromper el estado del gestor.
        """
        with self.assertRaises(EmpleadoFactoryError):
            EmpleadoFactory.crear_empleado(
                'ProjectManager', 'E099', 'X', ['Python', 2])
        self.assertEqual(self.gestor.empleados, [])

    # --- Caso 2: rechazar empleado duplicado
    def test_registrar_empleado_duplicado_lanza_value_error(self):
        dev = EmpleadoFactory.crear_empleado(
            'Desarrollador', 'E001', 'Ana', ['Python', 'Junior'])
        self.gestor.registrar_empleado(dev)
        # El segundo intento con el mismo código debe lanzar ``ValueError``.
        with self.assertRaises(ValueError):
            self.gestor.registrar_empleado(dev)
        # El estado del gestor no se altera (no se duplica).
        self.assertEqual(len(self.gestor.empleados), 1)

    # --- Caso 8: tarifas polimórficas
    def test_tarifas_polimorficas(self):
        """Cada subclase aplica su propio tarifario: ``Desarrollador``
        60, ``QA`` 50, ``Líder Técnico`` 90.
        """
        empleados = [
            EmpleadoFactory.crear_empleado(
                'Desarrollador', 'E001', 'Ana', ['Python', 'Junior']),
            EmpleadoFactory.crear_empleado(
                'QA', 'E002', 'Luis', ['Funcional', 'Manual']),
            EmpleadoFactory.crear_empleado(
                'LiderTecnico', 'E003', 'Marta', ['Python', 2]),
        ]
        # 2 horas: 2*60, 2*50, 2*90 → 120, 100, 180.
        self.assertEqual(
            [e.calcular_costo(2) for e in empleados],
            [120, 100, 180],
        )


if __name__ == '__main__':
    unittest.main()