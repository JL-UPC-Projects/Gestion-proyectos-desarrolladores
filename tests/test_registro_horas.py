"""Caso 7: rechazar registro de horas con valor no positivo."""
import unittest

from modelos.asignacion import Asignacion
from modelos.cliente import Cliente
from modelos.desarrollador import Desarrollador
from modelos.gestor_datos import GestorDatos
from modelos.presupuesto import Presupuesto
from modelos.proyecto import Proyecto
from modelos.registro_horas import RegistroHoras
from modelos.tarea import Tarea


class RegistroHorasTests(unittest.TestCase):
    """Cubre el rechazo de horas ≤ 0 (cero o negativas)."""

    def setUp(self):
        self.gestor = GestorDatos()
        self.empleado = Desarrollador('E001', 'Ana', 'Python', 'Junior')
        self.cliente = Cliente('C001', 'Cliente', 'demo@example.com')
        self.proyecto = Proyecto('P001', 'Proyecto', self.cliente, Presupuesto(1000))
        self.gestor.registrar_empleado(self.empleado)
        self.gestor.registrar_cliente(self.cliente)
        self.gestor.registrar_proyecto(self.proyecto)
        Asignacion(self.empleado, self.proyecto, '2026-09-28', 20, 'Dev').registrar_asignacion()
        self.tarea = Tarea('T001', 'Tarea', self.proyecto, self.empleado)
        self.tarea.registrar_tarea()

    def test_rechaza_horas_negativas(self):
        """Horas ≤ 0 disparan ``ValueError`` al construir el registro."""
        for invalido in [0, -1, -2.5]:
            with self.subTest(horas=invalido):
                with self.assertRaises(ValueError):
                    RegistroHoras(self.tarea, self.empleado, '2026-09-29', invalido)


if __name__ == '__main__':
    unittest.main()