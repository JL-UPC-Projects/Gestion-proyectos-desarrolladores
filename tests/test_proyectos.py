"""Caso 3: rechazar un proyecto cuyo código de cliente no está registrado."""
import unittest

from modelos.cliente import Cliente
from modelos.gestor_datos import GestorDatos
from modelos.presupuesto import Presupuesto
from modelos.proyecto import Proyecto


class ProyectoTests(unittest.TestCase):
    """Cubre la regla: ``RegClienteUn proyecto requiere un cliente ya registrado``."""

    def test_rechaza_proyecto_con_cliente_inexistente(self):
        """Si el cliente no está en el gestor, ``registrar_proyecto``
        lanza ``ValueError`` y no agrega el proyecto a la colección.
        """
        gestor = GestorDatos()
        cliente_ajeno = Cliente('C-X', 'Otro', 'otro@example.com')
        proyecto = Proyecto('P001', 'Sin cliente', cliente_ajeno, Presupuesto(1000))

        with self.assertRaises(ValueError):
            gestor.registrar_proyecto(proyecto)
        self.assertEqual(gestor.proyectos, [])

    def test_acepta_proyecto_con_cliente_registrado(self):
        """Camino feliz: tras registrar el cliente, el proyecto se acepta."""
        gestor = GestorDatos()
        cliente = Cliente('C001', 'Cliente académico', 'demo@example.com')
        gestor.registrar_cliente(cliente)
        proyecto = Proyecto('P001', 'Proyecto', cliente, Presupuesto(500))
        gestor.registrar_proyecto(proyecto)
        self.assertEqual(gestor.proyectos, [proyecto])


if __name__ == '__main__':
    unittest.main()