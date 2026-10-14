"""Casos 9, 10 y 11: cálculo de costo, saldo positivo y presupuesto excedido."""
import unittest

from modelos.asignacion import Asignacion
from modelos.calculadora_costos import CalculadoraCostos
from modelos.cliente import Cliente
from modelos.desarrollador import Desarrollador
from modelos.lider_tecnico import LiderTecnico
from modelos.presupuesto import Presupuesto
from modelos.proyecto import Proyecto
from modelos.qa import QA
from modelos.registro_horas import RegistroHoras
from modelos.tarea import Tarea


class CalculadoraCostosTests(unittest.TestCase):
    """Verifica los valores académicos esperados (400/600/-100)."""

    def setUp(self):
        # Mismo escenario que la demo: presupuesto 1000, 2h por cada empleado.
        self.cliente = Cliente('C001', 'Cliente', 'demo@example.com')
        self.proyecto = Proyecto('P001', 'Proyecto', self.cliente, Presupuesto(1000))
        self.empleados = [
            Desarrollador('E001', 'Ana', 'Python', 'Junior'),
            QA('E002', 'Luis', 'Funcional', 'Manual'),
            LiderTecnico('E003', 'Marta', 'Python', 2),
        ]
        for indice, empleado in enumerate(self.empleados, start=1):
            Asignacion(empleado, self.proyecto, '2026-09-28', 16,
                       type(empleado).__name__).registrar_asignacion()
            tarea = Tarea(f'T{indice:03}', f'Actividad {indice}', self.proyecto, empleado)
            tarea.registrar_tarea()
            RegistroHoras(tarea, empleado, '2026-09-29', 2).registrar_horas()

    def test_calcular_costo_acumulado_es_400(self):
        """Caso 9: 2h Desarrollador (120) + 2h QA (100) + 2h LiderTecnico (180) = 400."""
        self.assertEqual(CalculadoraCostos.calcular_costo_proyecto(self.proyecto), 400)

    def test_saldo_positivo_con_presupuesto_1000(self):
        """Caso 10: saldo = presupuesto (1000) − costo ejecutado (400) = 600."""
        self.assertEqual(CalculadoraCostos.calcular_saldo(self.proyecto), 600)
        self.assertTrue(CalculadoraCostos.comparar_presupuesto(self.proyecto))

    def test_presupuesto_excedido_con_presupuesto_300(self):
        """Caso 11: con presupuesto 300 el saldo es -100 y retorna ``False``."""
        self.proyecto.presupuesto.monto_total = 300
        self.assertEqual(CalculadoraCostos.calcular_saldo(self.proyecto), -100)
        self.assertFalse(CalculadoraCostos.comparar_presupuesto(self.proyecto))
        self.assertTrue(self.proyecto.presupuesto.verificar_exceso())


if __name__ == '__main__':
    unittest.main()