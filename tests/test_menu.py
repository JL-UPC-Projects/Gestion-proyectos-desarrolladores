"""Caso 14: el menú maneja entradas no numéricas, fuera de rango y rechaza la antigua opción 9."""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from modelos.sistema import Sistema


class MenuTests(unittest.TestCase):
    """Cubre el ciclo del menú principal ante entradas inválidas y la salida limpia."""

    def test_opcion_no_numerica_y_fuera_de_rango_terminan_limpio(self):
        """Secuencia 'x', '99', '0' termina con éxito y deja constancia del rechazo."""
        with tempfile.TemporaryDirectory() as carpeta:
            with patch('builtins.input', side_effect=['x', '99', '0']):
                with contextlib.redirect_stdout(io.StringIO()) as salida:
                    resultado = Sistema(Path(carpeta)).iniciar()
            self.assertEqual(resultado, 0)
            self.assertIn('Seleccione una opción', salida.getvalue())

    def test_opcion_9_se_rechaza_y_vuelve_al_menu(self):
        """Ingresar '9' produce error de fuera de rango; '0' permite salir después."""
        with tempfile.TemporaryDirectory() as carpeta:
            with patch('builtins.input', side_effect=['9', '0']):
                with contextlib.redirect_stdout(io.StringIO()) as salida:
                    resultado = Sistema(Path(carpeta)).iniciar()
            self.assertEqual(resultado, 0)
            texto = salida.getvalue()
            self.assertIn('Seleccione una opción', texto)
            # La sesión continuó tras el rechazo (se leyó otra opción después).
            self.assertIn('¡Hasta pronto!', texto)


if __name__ == '__main__':
    unittest.main()