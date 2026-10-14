"""Punto de entrada: ejecuta el sistema desde la raíz con ``python main.py``."""
import argparse
from modelos.sistema import Sistema


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gestión de proyectos — sistema académico FP2 (UPC)')
    parser.add_argument('--datos', default='datos', help='Directorio de los archivos JSON de persistencia')
    args = parser.parse_args()
    raise SystemExit(Sistema(args.datos).iniciar())
