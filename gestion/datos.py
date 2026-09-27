"""Persistencia preliminar de empleados, clientes y proyectos en un snapshot JSON."""
import json
from pathlib import Path
from .modelos import Cliente, Proyecto, Presupuesto, Desarrollador, QA, LiderTecnico


class GestorDatos:
    def __init__(self, ruta_datos='datos/catalogos.json'):
        self.ruta_datos = Path(ruta_datos)
        self.empleados = []
        self.clientes = []
        self.proyectos = []
        self._lectura_correcta = False

    def cargar_datos(self):
        self._lectura_correcta = False
        if not self.ruta_datos.exists():
            self.empleados, self.clientes, self.proyectos = [], [], []
            self._lectura_correcta = True
            return
        try:
            data = json.loads(self.ruta_datos.read_text(encoding='utf-8'))
            if data['version'] != 1: raise ValueError('Versión JSON no compatible.')
            temporal = GestorDatos(self.ruta_datos)
            tipos = {'Desarrollador': Desarrollador, 'QA': QA, 'LiderTecnico': LiderTecnico}
            for fila in data['empleados']:
                temporal.registrar_empleado(tipos[fila['tipo']](*fila['datos']))
            for fila in data['clientes']:
                temporal.registrar_cliente(Cliente(*fila))
            for fila in data['proyectos']:
                cliente = temporal.buscar_cliente(fila['cliente'])
                if cliente is None: raise ValueError('Cliente inexistente en JSON.')
                temporal.registrar_proyecto(Proyecto(fila['codigo'], fila['nombre'],
                                                    cliente, Presupuesto(fila['presupuesto'])))
            self.empleados = temporal.empleados
            self.clientes = temporal.clientes
            self.proyectos = temporal.proyectos
            self._lectura_correcta = True
        except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
            raise ValueError(f'No se pudieron cargar los datos; archivo conservado: {error}') from error

    def guardar_datos(self):
        if not self._lectura_correcta:
            raise ValueError('Primero debe cargar los datos correctamente.')
        # No permitir que un guardado de catálogos aparente persistir otros módulos.
        if any(p.asignaciones or p.tareas or p.estado != 'Planificado' or
               p.presupuesto.monto_ejecutado != 0 for p in self.proyectos):
            raise ValueError('Este preliminar solo persiste catálogos; los movimientos son en memoria.')
        empleados = []
        for e in self.empleados:
            if isinstance(e, Desarrollador): extras = [e.lenguaje_principal, e.nivel]
            elif isinstance(e, QA): extras = [e.tipo_prueba, e.herramienta]
            elif isinstance(e, LiderTecnico): extras = [e.tecnologia_principal, e.equipo_a_cargo]
            else: raise ValueError('Tipo de empleado no admitido.')
            empleados.append({'tipo': type(e).__name__, 'datos': [e.codigo, e.nombre, *extras]})
        data = {'version': 1, 'empleados': empleados,
                'clientes': [[c.codigo, c.razon_social, c.contacto] for c in self.clientes],
                'proyectos': [{'codigo': p.codigo, 'nombre': p.nombre, 'cliente': p.cliente.codigo,
                               'presupuesto': p.presupuesto.monto_total} for p in self.proyectos]}
        self.ruta_datos.parent.mkdir(parents=True, exist_ok=True)
        temporal = self.ruta_datos.with_suffix('.tmp')
        temporal.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
        temporal.replace(self.ruta_datos)

    @staticmethod
    def _registrar(coleccion, objeto):
        if any(e.codigo == objeto.codigo for e in coleccion):
            raise ValueError('El código ya existe.')
        coleccion.append(objeto)

    def registrar_empleado(self, e): self._registrar(self.empleados, e)

    def buscar_empleado(self, codigo):
        return next((e for e in self.empleados if e.codigo == codigo.strip()), None)

    def registrar_cliente(self, c): self._registrar(self.clientes, c)

    def buscar_cliente(self, codigo):
        return next((c for c in self.clientes if c.codigo == codigo.strip()), None)

    def registrar_proyecto(self, p):
        if p.cliente not in self.clientes: raise ValueError('Debe registrar primero al cliente.')
        self._registrar(self.proyectos, p)
