"""Casos 12 y 13: guardar/recuperar y JSON corrupto."""
import tempfile
import unittest
from datetime import date as _date_cls

from modelos.asignacion import Asignacion
from modelos.cliente import Cliente
from modelos.desarrollador import Desarrollador
from modelos.gestor_datos import GestorDatos, PersistenciaError
from modelos.lider_tecnico import LiderTecnico
from modelos.presupuesto import Presupuesto
from modelos.proyecto import Proyecto
from modelos.qa import QA
from modelos.registro_horas import RegistroHoras
from modelos.tarea import Tarea


class PersistenciaTests(unittest.TestCase):
    """Persistencia en los seis JSON con reconstrucción de relaciones."""

    def setUp(self):
        # Directorio temporal aislado por test.
        self._tmp = tempfile.TemporaryDirectory()
        self.gestor = GestorDatos(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_guardar_y_recuperar_reconstruye_relaciones(self):
        """Caso 12: guardar y recuperar preserva referencias compartidas."""
        g = self.gestor
        g.cargar_datos()

        dev = Desarrollador('E001', 'Ana', 'Python', 'Junior')
        qa = QA('E002', 'Luis', 'Funcional', 'Manual')
        lider = LiderTecnico('E003', 'Marta', 'Python', 2)
        g.registrar_empleado(dev)
        g.registrar_empleado(qa)
        g.registrar_empleado(lider)

        cliente = Cliente('C001', 'Cliente', 'demo@example.com')
        g.registrar_cliente(cliente)

        proyecto = Proyecto('P001', 'Proyecto', cliente, Presupuesto(1000))
        g.registrar_proyecto(proyecto)

        # Asignación, tarea y registro pasan por el gestor para que las
        # seis listas queden pobladas antes de persistir.
        asignacion = Asignacion(dev, proyecto, '2026-09-28', 20, 'Dev')
        asignacion.registrar_asignacion()
        g.registrar_asignacion(asignacion)
        tarea = Tarea('T001', 'Tarea', proyecto, dev)
        tarea.registrar_tarea()
        g.registrar_tarea(tarea)
        registro = RegistroHoras(tarea, dev, '2026-09-29', 2)
        registro.registrar_horas()
        g.registrar_registro_horas(registro)

        g.guardar_datos()

        otro = GestorDatos(self._tmp.name)
        otro.cargar_datos()

        self.assertEqual(len(otro.empleados), 3)
        self.assertEqual(len(otro.clientes), 1)
        self.assertEqual(len(otro.proyectos), 1)
        self.assertEqual(len(otro.asignaciones), 1)
        self.assertEqual(len(otro.tareas), 1)
        self.assertEqual(len(otro.registros), 1)

        # Las relaciones se reconstruyen como identidad compartida.
        self.assertIs(otro.proyectos[0].cliente, otro.clientes[0])
        self.assertIs(otro.asignaciones[0].empleado, otro.buscar_empleado('E001'))
        self.assertIs(otro.asignaciones[0].proyecto, otro.proyectos[0])
        self.assertIs(otro.tareas[0].responsable, otro.buscar_empleado('E001'))
        self.assertIs(otro.tareas[0].proyecto, otro.proyectos[0])
        self.assertIs(otro.registros[0].tarea, otro.buscar_tarea('T001'))
        self.assertIs(otro.registros[0].empleado, otro.buscar_empleado('E001'))

        # El método polimórfico sigue funcionando tras la reconstrucción.
        self.assertEqual(otro.buscar_empleado('E001').calcular_costo(2), 120)
        self.assertEqual(otro.buscar_empleado('E002').calcular_costo(2), 100)
        self.assertEqual(otro.buscar_empleado('E003').calcular_costo(2), 180)

        # La fecha de emisión no se valida porque los JSON no la guardan.
        assert _date_cls  # noqa: F401 — uso explícito para no perder import.

    def test_json_corropo_lanza_excepcion_y_conserva_archivo(self):
        """Caso 13: JSON corrupto lanza ``PersistenciaError`` sin sobreescribirlo."""
        # Escribimos un JSON inválido manualmente.
        ruta_empleados = self.gestor._ruta(GestorDatos.ARCHIVO_EMPLEADOS)
        ruta_empleados.parent.mkdir(parents=True, exist_ok=True)
        ruta_empleados.write_text('{invalido', encoding='utf-8')

        with self.assertRaises(PersistenciaError):
            self.gestor.cargar_datos()

        # El archivo original permanece intacto (no se escribió nada encima).
        self.assertEqual(ruta_empleados.read_text(encoding='utf-8'), '{invalido')


if __name__ == '__main__':
    unittest.main()