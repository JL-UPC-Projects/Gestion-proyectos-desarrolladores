"""Ejecutar desde la raíz: python main.py."""
import argparse
from gestion.sistema import Sistema

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gestión de proyectos — preliminar UPC')
    parser.add_argument('--datos', default='datos/catalogos.json', help='Ruta del archivo de catálogos')
    args = parser.parse_args()
    raise SystemExit(Sistema(args.datos).iniciar())
