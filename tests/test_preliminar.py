import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from gestion.datos import GestorDatos
from gestion.modelos import (Desarrollador, QA, LiderTecnico, Cliente, Proyecto,
                             Presupuesto, Asignacion, Tarea, RegistroHoras, CalculadoraCostos)
from gestion.sistema import Sistema
from demo import ejecutar_demo


class PreliminarTests(unittest.TestCase):
    def setUp(self):
        self.e = Desarrollador('E1', 'Ana', 'Python', 'Junior')
        self.c = Cliente('C1', 'Cliente ficticio', 'demo@example.com')
        self.p = Proyecto('P1', 'Ejemplo', self.c, Presupuesto(1000))

    def test_tarifas_polimorficas(self):
        empleados = [self.e, QA('E2', 'Luis', 'Manual', 'Consola'), LiderTecnico('E3', 'Marta', 'Python', 2)]
        self.assertEqual([e.calcular_costo(2) for e in empleados], [120, 100, 180])

    def test_horas_no_validas(self):
        for horas in [0, -2, 'nan', 'inf']:
            with self.subTest(horas=horas), self.assertRaises(ValueError):
                self.e.calcular_costo(horas)

    def test_limite_semanal_y_modificacion(self):
        a = Asignacion(self.e, self.p, '2026-09-28', 20, 'Dev'); a.registrar_asignacion()
        p2 = Proyecto('P2', 'Otro', self.c, Presupuesto(1000))
        b = Asignacion(self.e, p2, '2026-09-28', 28, 'Dev'); b.registrar_asignacion()
        self.assertEqual(self.e.horas_disponibles('2026-09-28'), 0)
        with self.assertRaises(ValueError): b.modificar_horas(29)
        self.assertEqual(b.horas_semanales, 28)
        a.finalizar_asignacion()
        self.assertEqual(self.e.horas_disponibles('2026-09-28'), 20)

    def test_duplicidad_asignacion(self):
        Asignacion(self.e, self.p, '2026-09-28', 20, 'Dev').registrar_asignacion()
        with self.assertRaises(ValueError):
            Asignacion(self.e, self.p, '2026-09-28', 10, 'Dev').registrar_asignacion()

    def test_semana_independiente(self):
        for semana in ['2026-09-28', '2026-10-05']:
            Asignacion(self.e, self.p, semana, 48, 'Dev').registrar_asignacion()
        self.assertEqual(self.e.horas_disponibles('2026-10-12'), 48)

    def test_tarea_sin_asignacion(self):
        with self.assertRaises(ValueError): Tarea('T1', 'Tarea', self.p, self.e)

    def test_horas_fuera_semana(self):
        Asignacion(self.e, self.p, '2026-09-28', 20, 'Dev').registrar_asignacion()
        t = Tarea('T1', 'Tarea', self.p, self.e); t.registrar_tarea()
        with self.assertRaises(ValueError): RegistroHoras(t, self.e, '2026-10-06', 2).registrar_horas()

    def test_demo_y_sobrecosto(self):
        with contextlib.redirect_stdout(io.StringIO()): p = ejecutar_demo()
        self.assertEqual(CalculadoraCostos.calcular_costo_proyecto(p), 400)
        self.assertEqual(CalculadoraCostos.calcular_saldo(p), 600)
        p.presupuesto.monto_total = 300
        self.assertEqual(CalculadoraCostos.calcular_saldo(p), -100)
        self.assertFalse(CalculadoraCostos.comparar_presupuesto(p))

    def test_persistencia_reconstruye_cliente(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / 'catalogos.json'
            g = GestorDatos(ruta); g.cargar_datos()
            g.registrar_empleado(self.e); g.registrar_cliente(self.c); g.registrar_proyecto(self.p)
            g.guardar_datos()
            otro = GestorDatos(ruta); otro.cargar_datos()
            self.assertIs(otro.proyectos[0].cliente, otro.clientes[0])
            self.assertEqual(otro.empleados[0].calcular_costo(2), 120)

    def test_json_corrupto_no_se_sobrescribe(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / 'catalogos.json'; ruta.write_text('{invalido')
            g = GestorDatos(ruta)
            with self.assertRaises(ValueError): g.cargar_datos()
            with self.assertRaises(ValueError): g.guardar_datos()
            self.assertEqual(ruta.read_text(), '{invalido')

    def test_codigo_duplicado(self):
        g = GestorDatos(); g.registrar_empleado(self.e)
        with self.assertRaises(ValueError): g.registrar_empleado(self.e)

    def test_menu_recupera_opcion_invalida(self):
        with tempfile.TemporaryDirectory() as carpeta, patch('builtins.input', side_effect=['x', '99', '0']):
            with contextlib.redirect_stdout(io.StringIO()) as salida:
                resultado = Sistema(Path(carpeta) / 'catalogos.json').iniciar()
            self.assertEqual(resultado, 0)
            self.assertIn('Seleccione una opción', salida.getvalue())

    def test_no_simula_persistencia_de_movimientos(self):
        with tempfile.TemporaryDirectory() as carpeta:
            g = GestorDatos(Path(carpeta) / 'catalogos.json'); g.cargar_datos()
            g.registrar_cliente(self.c); g.registrar_proyecto(self.p)
            Asignacion(self.e, self.p, '2026-09-28', 2, 'Dev').registrar_asignacion()
            with self.assertRaises(ValueError): g.guardar_datos()


if __name__ == '__main__': unittest.main()
