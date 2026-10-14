"""Casos 4, 5, 6: reglas de capacidad (≤48h) y duplicidad semanal."""
import unittest

from modelos.asignacion import Asignacion
from modelos.cliente import Cliente
from modelos.desarrollador import Desarrollador
from modelos.gestor_datos import GestorDatos
from modelos.presupuesto import Presupuesto
from modelos.proyecto import Proyecto


class AsignacionTests(unittest.TestCase):
    """Cubre las reglas de 48 horas semanales y de unicidad por
    empleado/proyecto/semana.
    """

    def setUp(self):
        self.gestor = GestorDatos()
        self.empleado = Desarrollador('E001', 'Ana', 'Python', 'Junior')
        self.cliente = Cliente('C001', 'Cliente', 'demo@example.com')
        self.proyecto = Proyecto('P001', 'Proyecto', self.cliente, Presupuesto(1000))
        self.gestor.registrar_empleado(self.empleado)
        self.gestor.registrar_cliente(self.cliente)
        self.gestor.registrar_proyecto(self.proyecto)

    # --- Caso 4: 20h + 28h = 48h OK
    def test_acepta_asignacion_dentro_de_48_horas(self):
        """Dos asignaciones que suman 48h deben registrarse sin error."""
        a = Asignacion(self.empleado, self.proyecto, '2026-09-28', 20, 'Dev')
        a.registrar_asignacion()
        segundo = Proyecto('P002', 'Otro', self.cliente, Presupuesto(1000))
        self.gestor.registrar_proyecto(segundo)
        b = Asignacion(self.empleado, segundo, '2026-09-28', 28, 'Dev')
        b.registrar_asignacion()
        self.assertEqual(self.empleado.horas_disponibles('2026-09-28'), 0)

    # --- Caso 5: 20h + 29h > 48h falla
    def test_rechaza_asignacion_que_excede_48_horas(self):
        """La segunda asignación de 29h supera la capacidad (20+29=49)."""
        a = Asignacion(self.empleado, self.proyecto, '2026-09-28', 20, 'Dev')
        a.registrar_asignacion()
        segundo = Proyecto('P002', 'Otro', self.cliente, Presupuesto(1000))
        self.gestor.registrar_proyecto(segundo)
        b = Asignacion(self.empleado, segundo, '2026-09-28', 29, 'Dev')
        with self.assertRaises(ValueError):
            b.registrar_asignacion()
        # La asignación rechazada no queda activa.
        self.assertEqual(b.estado, 'Pendiente')

    # --- Caso 6: asignación semanal duplicada
    def test_rechaza_asignacion_semanal_duplicada(self):
        """Dos veces la misma semana/empleado/proyecto debe fallar."""
        Asignacion(self.empleado, self.proyecto, '2026-09-28', 10, 'Dev').registrar_asignacion()
        with self.assertRaises(ValueError):
            Asignacion(self.empleado, self.proyecto, '2026-09-28', 10, 'Dev').registrar_asignacion()


if __name__ == '__main__':
    unittest.main()

    