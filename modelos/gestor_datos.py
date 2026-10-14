"""GestorDatos: persistencia del sistema en seis archivos JSON separados."""
import json
from pathlib import Path

from modelos.empleado import Empleado
from modelos.cliente import Cliente
from modelos.presupuesto import Presupuesto
from modelos.proyecto import Proyecto
from modelos.asignacion import Asignacion
from modelos.tarea import Tarea
from modelos.registro_horas import RegistroHoras


class PersistenciaError(ValueError):
    """No se pudo cargar o guardar el estado; el archivo no se altera."""


class GestorDatos:
    """Mantiene en memoria las seis colecciones y las persiste en JSON."""

    # Nombres de archivo para cada colección; se resuelven contra ``ruta_datos``.
    ARCHIVO_EMPLEADOS = 'empleados.json'
    ARCHIVO_CLIENTES = 'clientes.json'
    ARCHIVO_PROYECTOS = 'proyectos.json'
    ARCHIVO_ASIGNACIONES = 'asignaciones.json'
    ARCHIVO_TAREAS = 'tareas.json'
    ARCHIVO_REGISTRO_HORAS = 'registro_horas.json'

    def __init__(self, ruta_datos='datos'):
        self.ruta_datos = Path(ruta_datos)
        self.empleados = []
        self.clientes = []
        self.proyectos = []
        self.asignaciones = []
        self.tareas = []
        self.registros = []
        self._lectura_correcta = False

    def cargar_datos(self):
        """Carga colecciones en orden para reconstruir referencias cruzadas."""
        try:
            self.empleados = self._cargar_empleados()
            self.clientes = self._cargar_clientes()
            self.proyectos = self._cargar_proyectos()
            self.asignaciones = self._cargar_asignaciones()
            self.tareas = self._cargar_tareas()
            self.registros = self._cargar_registros()
            self._lectura_correcta = True
        except PersistenciaError:
            # Propagar la excepción sin marcar el gestor como listo.
            raise
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise PersistenciaError(
                f'No se pudieron cargar los datos; archivo conservado: {error}'
            ) from error

    def guardar_datos(self):
        """Persiste el estado en los seis JSON. Escritura atómica."""
        if not self._lectura_correcta:
            raise PersistenciaError('Primero debe cargar los datos correctamente.')
        try:
            self._guardar_empleados()
            self._guardar_clientes()
            self._guardar_proyectos()
            self._guardar_asignaciones()
            self._guardar_tareas()
            self._guardar_registros()
        except OSError as error:
            raise PersistenciaError(f'No se pudo escribir el estado: {error}') from error

    def _ruta(self, nombre):
        return self.ruta_datos / nombre

    def _leer_json(self, nombre):
        """Devuelve [] si no existe; lanza ``PersistenciaError`` si está corrupto (archivo intacto)."""
        ruta = self._ruta(nombre)
        if not ruta.exists():
            return []
        try:
            contenido = ruta.read_text(encoding='utf-8')
            return json.loads(contenido)
        except (OSError, json.JSONDecodeError) as error:
            raise PersistenciaError(
                f'Archivo {nombre} corrupto o ilegible ({error}); se conserva intacto.'
            ) from error

    def _cargar_empleados(self):
        """Reconstruye cada subclase a partir del campo ``tipo``."""
        from modelos.desarrollador import Desarrollador
        from modelos.qa import QA
        from modelos.lider_tecnico import LiderTecnico

        tipos = {'Desarrollador': Desarrollador, 'QA': QA, 'LiderTecnico': LiderTecnico}
        empleados = []
        for fila in self._leer_json(self.ARCHIVO_EMPLEADOS):
            tipo = fila['tipo']
            if tipo not in tipos:
                raise PersistenciaError(f'Tipo de empleado desconocido: {tipo!r}.')
            datos = fila['datos']
            empleados.append(tipos[tipo](*datos))
        return empleados

    def _cargar_clientes(self):
        return [Cliente(fila['codigo'], fila['razon_social'], fila['contacto'])
                for fila in self._leer_json(self.ARCHIVO_CLIENTES)]

    def _cargar_proyectos(self):
        proyectos = []
        for fila in self._leer_json(self.ARCHIVO_PROYECTOS):
            cliente = self.buscar_cliente(fila['cliente_codigo'])
            if cliente is None:
                raise PersistenciaError(
                    f'Proyecto {fila["codigo"]!r} referencia al cliente '
                    f'{fila["cliente_codigo"]!r} que no existe.'
                )
            presupuesto = Presupuesto(fila['presupuesto_monto'])
            proyecto = Proyecto(fila['codigo'], fila['nombre'], cliente, presupuesto)
            proyecto.estado = fila.get('estado', proyecto.estado)
            proyectos.append(proyecto)
        return proyectos

    def _cargar_asignaciones(self):
        asignaciones = []
        for fila in self._leer_json(self.ARCHIVO_ASIGNACIONES):
            empleado = self.buscar_empleado(fila['empleado_codigo'])
            proyecto = self.buscar_proyecto(fila['proyecto_codigo'])
            if empleado is None:
                raise PersistenciaError(
                    f'Asignación referencia al empleado '
                    f'{fila["empleado_codigo"]!r} que no existe.'
                )
            if proyecto is None:
                raise PersistenciaError(
                    f'Asignación referencia al proyecto '
                    f'{fila["proyecto_codigo"]!r} que no existe.'
                )
            asignacion = Asignacion(
                empleado, proyecto, fila['semana'], fila['horas_semanales'], fila['rol'])
            # ``Asignacion.__init__`` arranca en 'Pendiente' y ``registrar_asignacion``
            # valida capacidad/disponible. Al reconstruir, saltamos esa validación
            # porque ya pasó en su sesión original y restauramos el estado.
            asignacion.estado = fila.get('estado', 'Activa')
            empleado._asignaciones.append(asignacion)
            proyecto.asignaciones.append(asignacion)
            asignaciones.append(asignacion)
        return asignaciones

    def _cargar_tareas(self):
        tareas = []
        for fila in self._leer_json(self.ARCHIVO_TAREAS):
            proyecto = self.buscar_proyecto(fila['proyecto_codigo'])
            if proyecto is None:
                raise PersistenciaError(
                    f'Tarea {fila["codigo"]!r} referencia al proyecto '
                    f'{fila["proyecto_codigo"]!r} que no existe.'
                )
            responsable = self.buscar_empleado(fila['responsable_codigo'])
            if responsable is None:
                raise PersistenciaError(
                    f'Tarea {fila["codigo"]!r} referencia al responsable '
                    f'{fila["responsable_codigo"]!r} que no existe.'
                )
            tarea = Tarea(fila['codigo'], fila['titulo'], proyecto, responsable)
            tarea.estado = fila.get('estado', 'Pendiente')
            # Se agrega al proyecto sin revalidar duplicados (la unicidad la
            # garantizó ``Tarea.registrar_tarea`` en su sesión original).
            proyecto.tareas.append(tarea)
            tareas.append(tarea)
        return tareas

    def _cargar_registros(self):
        registros = []
        for fila in self._leer_json(self.ARCHIVO_REGISTRO_HORAS):
            tarea = self.buscar_tarea(fila['tarea_codigo'])
            empleado = self.buscar_empleado(fila['empleado_codigo'])
            if tarea is None:
                raise PersistenciaError(
                    f'Registro referencia a la tarea {fila["tarea_codigo"]!r} '
                    f'que no existe.'
                )
            if empleado is None:
                raise PersistenciaError(
                    f'Registro referencia al empleado {fila["empleado_codigo"]!r} '
                    f'que no existe.'
                )
            registro = RegistroHoras(tarea, empleado, fila['fecha'], fila['horas'])
            tarea.registros.append(registro)
            registros.append(registro)
        return registros

    def _escribir_json(self, nombre, datos):
        """Escribe un JSON de forma atómica (tmp + replace)."""
        self.ruta_datos.mkdir(parents=True, exist_ok=True)
        destino = self._ruta(nombre)
        temporal = destino.with_suffix('.tmp')
        # ``allow_nan=False`` rechaza ``NaN``/``Infinity`` explícitamente.
        temporal.write_text(
            json.dumps(datos, ensure_ascii=False, indent=2, allow_nan=False),
            encoding='utf-8',
        )
        temporal.replace(destino)

    def _serializar_empleado(self, empleado):
        from modelos.desarrollador import Desarrollador
        from modelos.qa import QA
        from modelos.lider_tecnico import LiderTecnico

        if isinstance(empleado, Desarrollador):
            extras = [empleado.lenguaje_principal, empleado.nivel]
        elif isinstance(empleado, QA):
            extras = [empleado.tipo_prueba, empleado.herramienta]
        elif isinstance(empleado, LiderTecnico):
            extras = [empleado.tecnologia_principal, empleado.equipo_a_cargo]
        else:
            raise PersistenciaError(f'Tipo de empleado no admitido: {type(empleado).__name__}.')
        return {'tipo': type(empleado).__name__,
                'datos': [empleado.codigo, empleado.nombre, *extras]}

    def _guardar_empleados(self):
        self._escribir_json(
            self.ARCHIVO_EMPLEADOS,
            [self._serializar_empleado(e) for e in self.empleados],
        )

    def _guardar_clientes(self):
        self._escribir_json(
            self.ARCHIVO_CLIENTES,
            [{'codigo': c.codigo, 'razon_social': c.razon_social, 'contacto': c.contacto}
             for c in self.clientes],
        )

    def _guardar_proyectos(self):
        self._escribir_json(
            self.ARCHIVO_PROYECTOS,
            [{'codigo': p.codigo, 'nombre': p.nombre,
              'cliente_codigo': p.cliente.codigo,
              'presupuesto_monto': p.presupuesto.monto_total,
              'estado': p.estado}
             for p in self.proyectos],
        )

    def _guardar_asignaciones(self):
        self._escribir_json(
            self.ARCHIVO_ASIGNACIONES,
            [{'empleado_codigo': a.empleado.codigo,
              'proyecto_codigo': a.proyecto.codigo,
              'semana': a.semana,
              'horas_semanales': a.horas_semanales,
              'rol': a.rol,
              'estado': a.estado}
             for a in self.asignaciones],
        )

    def _guardar_tareas(self):
        self._escribir_json(
            self.ARCHIVO_TAREAS,
            [{'codigo': t.codigo,
              'titulo': t.titulo,
              'proyecto_codigo': t.proyecto.codigo,
              'responsable_codigo': t.responsable.codigo,
              'estado': t.estado}
             for t in self.tareas],
        )

    def _guardar_registros(self):
        self._escribir_json(
            self.ARCHIVO_REGISTRO_HORAS,
            [{'tarea_codigo': r.tarea.codigo,
              'empleado_codigo': r.empleado.codigo,
              'fecha': r.fecha,
              'horas': r.horas}
             for r in self.registros],
        )

    @staticmethod
    def _validar_codigo(codigo):
        if any(obj.codigo == codigo for obj in []):
            pass
        return codigo

    def _registrar(self, coleccion, objeto):
        if any(obj.codigo == objeto.codigo for obj in coleccion):
            raise ValueError(f'El código {objeto.codigo!r} ya existe.')
        coleccion.append(objeto)

    def registrar_empleado(self, empleado):
        if not isinstance(empleado, Empleado):
            raise ValueError('Solo se admiten instancias de Empleado.')
        self._registrar(self.empleados, empleado)

    def buscar_empleado(self, codigo):
        return next((e for e in self.empleados if e.codigo == codigo), None)

    def registrar_cliente(self, cliente):
        self._registrar(self.clientes, cliente)

    def buscar_cliente(self, codigo):
        return next((c for c in self.clientes if c.codigo == codigo), None)

    def registrar_proyecto(self, proyecto):
        if proyecto.cliente not in self.clientes:
            raise ValueError('Debe registrar primero al cliente.')
        self._registrar(self.proyectos, proyecto)

    def buscar_proyecto(self, codigo):
        return next((p for p in self.proyectos if p.codigo == codigo), None)

    def registrar_asignacion(self, asignacion):
        if asignacion.empleado not in self.empleados:
            raise ValueError('Debe registrar primero al empleado.')
        if asignacion.proyecto not in self.proyectos:
            raise ValueError('Debe registrar primero al proyecto.')
        self._registrar(self.asignaciones, asignacion)

    def buscar_asignacion(self, empleado_codigo, proyecto_codigo, semana):
        return next((a for a in self.asignaciones
                     if a.empleado.codigo == empleado_codigo
                     and a.proyecto.codigo == proyecto_codigo
                     and a.semana == semana), None)

    def registrar_tarea(self, tarea):
        if tarea.proyecto not in self.proyectos:
            raise ValueError('Debe registrar primero al proyecto.')
        self._registrar(self.tareas, tarea)

    def buscar_tarea(self, codigo):
        return next((t for t in self.tareas if t.codigo == codigo), None)

    def registrar_registro_horas(self, registro):
        if registro.tarea not in self.tareas:
            raise ValueError('Debe registrar primero la tarea.')
        if registro.empleado not in self.empleados:
            raise ValueError('Debe registrar primero al empleado.')
        self.registros.append(registro)