"""Sistema: orquestador del menú y de la persistencia."""
from datetime import date

from modelos.asignacion import Asignacion
from modelos.calculadora_costos import CalculadoraCostos
from modelos.cliente import Cliente
from modelos.desarrollador import Desarrollador
from modelos.empleado_factory import EmpleadoFactory
from modelos.gestor_datos import GestorDatos, PersistenciaError
from modelos.lider_tecnico import LiderTecnico
from modelos.menu_principal import MenuPrincipal
from modelos.presupuesto import Presupuesto
from modelos.proyecto import Proyecto
from modelos.qa import QA
from modelos.registro_horas import RegistroHoras
from modelos.reporte import Reporte
from modelos.tarea import Tarea


class Sistema:
    """Carga al iniciar, persiste antes de salir; cada operación con manejo de errores controlado."""

    def __init__(self, ruta_datos='datos'):
        self.menu = MenuPrincipal()
        self.gestor = GestorDatos(ruta_datos)

    def iniciar(self):
        try:
            self.gestor.cargar_datos()
        except PersistenciaError as error:
            print(error)
            return 1  # No continuar: podría sobrescribir datos ilegibles.
        while True:
            try:
                self.menu.mostrar_menu()
                opcion = self.menu.solicitar_opcion()
                if opcion == MenuPrincipal.OPCION_SALIR:
                    try:
                        self.gestor.guardar_datos()
                        print('Datos guardados. ¡Hasta pronto!')
                    except PersistenciaError as error:
                        print(f'Aviso al guardar: {error}')
                    return 0
                self.ejecutar_opcion(opcion)
            except (ValueError, OSError) as error:
                self.menu.mostrar_resultado(f'No se completó la operación: {error}')
            except (EOFError, KeyboardInterrupt):
                print('\nSesión interrumpida; se conservan los datos confirmados.')
                return 0

    def ejecutar_opcion(self, opcion):
        if opcion == MenuPrincipal.OPCION_EMPLEADOS:
            self._submenu_empleados()
        elif opcion == MenuPrincipal.OPCION_CLIENTES:
            self._submenu_clientes()
        elif opcion == MenuPrincipal.OPCION_PROYECTOS:
            self._submenu_proyectos()
        elif opcion == MenuPrincipal.OPCION_ASIGNACIONES:
            self._submenu_asignaciones()
        elif opcion == MenuPrincipal.OPCION_TAREAS:
            self._submenu_tareas()
        elif opcion == MenuPrincipal.OPCION_REGISTRO_HORAS:
            self._submenu_registro_horas()
        elif opcion == MenuPrincipal.OPCION_COSTOS:
            self._submenu_costos()
        elif opcion == MenuPrincipal.OPCION_REPORTES:
            self._submenu_reportes()
        else:
            raise ValueError('Seleccione una opción del menú (0-8).')

    def _leer_submenu(self, maximo):
        """Lee la opción de un submenú (1..maximo, 0=volver)."""
        opcion = int(input('Opción: '))
        if opcion == 0:
            return 0
        if opcion < 0 or opcion > maximo:
            raise ValueError(f'Seleccione una opción del submenú (0-{maximo}).')
        return opcion

    def _submenu_empleados(self):
        while True:
            print('\n--- Empleados ---')
            print('1. Registrar')
            print('2. Listar')
            print('3. Buscar y calcular importe')
            print('0. Volver al menú principal')
            opcion = self._leer_submenu(3)
            if opcion == 0:
                return
            if opcion == 1:
                self._registrar_empleado()
            elif opcion == 2:
                self._listar_empleados()
            elif opcion == 3:
                self._buscar_empleado()

    def _submenu_clientes(self):
        while True:
            print('\n--- Clientes ---')
            print('1. Registrar')
            print('2. Listar')
            print('0. Volver al menú principal')
            opcion = self._leer_submenu(2)
            if opcion == 0:
                return
            if opcion == 1:
                self._registrar_cliente()
            elif opcion == 2:
                self._listar_clientes()

    def _submenu_proyectos(self):
        while True:
            print('\n--- Proyectos ---')
            print('1. Registrar')
            print('2. Listar')
            print('0. Volver al menú principal')
            opcion = self._leer_submenu(2)
            if opcion == 0:
                return
            if opcion == 1:
                self._registrar_proyecto()
            elif opcion == 2:
                self._listar_proyectos()

    def _submenu_asignaciones(self):
        while True:
            print('\n--- Asignaciones ---')
            print('1. Registrar')
            print('2. Listar')
            print('0. Volver al menú principal')
            opcion = self._leer_submenu(2)
            if opcion == 0:
                return
            if opcion == 1:
                self._registrar_asignacion()
            elif opcion == 2:
                self._listar_asignaciones()

    def _submenu_tareas(self):
        while True:
            print('\n--- Tareas ---')
            print('1. Registrar')
            print('2. Listar')
            print('3. Actualizar estado')
            print('0. Volver al menú principal')
            opcion = self._leer_submenu(3)
            if opcion == 0:
                return
            if opcion == 1:
                self._registrar_tarea()
            elif opcion == 2:
                self._listar_tareas()
            elif opcion == 3:
                self._actualizar_estado_tarea()

    def _submenu_registro_horas(self):
        while True:
            print('\n--- Registro de horas ---')
            print('1. Registrar horas')
            print('2. Listar')
            print('0. Volver al menú principal')
            opcion = self._leer_submenu(2)
            if opcion == 0:
                return
            if opcion == 1:
                self._registrar_horas()
            elif opcion == 2:
                self._listar_registros()

    def _submenu_costos(self):
        while True:
            print('\n--- Costos y presupuestos ---')
            print('1. Calcular costo del proyecto')
            print('2. Calcular saldo')
            print('3. Comparar presupuesto')
            print('0. Volver al menú principal')
            opcion = self._leer_submenu(3)
            if opcion == 0:
                return
            if opcion == 1:
                self._calcular_costo()
            elif opcion == 2:
                self._calcular_saldo()
            elif opcion == 3:
                self._comparar_presupuesto()

    def _submenu_reportes(self):
        while True:
            print('\n--- Reportes ---')
            print('1. Reporte de proyectos')
            print('2. Reporte de empleados')
            print('3. Reporte de tareas')
            print('4. Reporte de costos')
            print('0. Volver al menú principal')
            opcion = self._leer_submenu(4)
            if opcion == 0:
                return
            reporte = Reporte(self.gestor)
            if opcion == 1:
                lineas = reporte.generar_reporte_proyectos()
                self._imprimir_lista(lineas, 'Sin proyectos.')
            elif opcion == 2:
                lineas = reporte.generar_reporte_empleados()
                self._imprimir_lista(lineas, 'Sin empleados.')
            elif opcion == 3:
                lineas = reporte.generar_reporte_tareas()
                self._imprimir_lista(lineas, 'Sin tareas.')
            elif opcion == 4:
                lineas = reporte.generar_reporte_costos()
                self._imprimir_lista(lineas, 'Sin proyectos.')

    def _registrar_empleado(self):
        print('Tipo: 1 Desarrollador | 2 QA | 3 LiderTecnico')
        tipo_opcion = input('Tipo: ').strip()
        tipos = {'1': 'Desarrollador', '2': 'QA', '3': 'LiderTecnico'}
        if tipo_opcion not in tipos:
            raise ValueError('Tipo de empleado inválido (use 1, 2 o 3).')
        tipo = tipos[tipo_opcion]
        codigo = input('Código: ')
        nombre = input('Nombre: ')
        if tipo == 'Desarrollador':
            extras = [input('Lenguaje principal: '), input('Nivel: ')]
        elif tipo == 'QA':
            extras = [input('Tipo de prueba: '), input('Herramienta: ')]
        else:
            extras = [input('Tecnología principal: '), input('Cantidad a cargo: ')]
        # El Factory concentra la decisión de subclase; los tipos válidos son
        # 'Desarrollador' / 'QA' / 'LiderTecnico' ya garantizados arriba.
        empleado = EmpleadoFactory.crear_empleado(tipo, codigo, nombre, extras)
        self._guardar(self.gestor.empleados, empleado, self.gestor.registrar_empleado)

    def _listar_empleados(self):
        self._imprimir_lista(
            [f'{e.codigo} | {e.nombre} | {type(e).__name__}' for e in self.gestor.empleados],
            'Sin empleados registrados.',
        )

    def _buscar_empleado(self):
        codigo = input('Código: ')
        empleado = self.gestor.buscar_empleado(codigo)
        if empleado is None:
            raise ValueError(f'Empleado {codigo!r} no encontrado.')
        horas = input('Horas para cálculo: ')
        importe = empleado.calcular_costo(horas)
        print(f'{empleado.nombre} ({type(empleado).__name__}) — S/ {importe:.2f}')

    def _registrar_cliente(self):
        cliente = Cliente(
            input('Código: '),
            input('Razón social: '),
            input('Contacto: '),
        )
        self._guardar(self.gestor.clientes, cliente, self.gestor.registrar_cliente)

    def _listar_clientes(self):
        self._imprimir_lista(
            [c.mostrar_resumen() for c in self.gestor.clientes],
            'Sin clientes registrados.',
        )

    def _registrar_proyecto(self):
        cliente_codigo = input('Código de cliente existente: ')
        cliente = self.gestor.buscar_cliente(cliente_codigo)
        if cliente is None:
            raise ValueError(f'Cliente {cliente_codigo!r} no encontrado.')
        proyecto = Proyecto(
            input('Código de proyecto: '),
            input('Nombre: '),
            cliente,
            Presupuesto(input('Presupuesto S/: ')),
        )
        self._guardar(self.gestor.proyectos, proyecto, self.gestor.registrar_proyecto)

    def _listar_proyectos(self):
        self._imprimir_lista(
            [f'{p.codigo} | {p.nombre} | {p.estado}' for p in self.gestor.proyectos],
            'Sin proyectos registrados.',
        )

    def _registrar_asignacion(self):
        empleado = self.gestor.buscar_empleado(input('Código de empleado: '))
        if empleado is None:
            raise ValueError('Empleado no encontrado.')
        proyecto = self.gestor.buscar_proyecto(input('Código de proyecto: '))
        if proyecto is None:
            raise ValueError('Proyecto no encontrado.')
        semana = input('Semana (lunes ISO, YYYY-MM-DD): ')
        horas = input('Horas semanales: ')
        rol = input('Rol: ')
        # ``Asignacion.registrar_asignacion`` valida capacidad y duplicidad.
        asignacion = Asignacion(empleado, proyecto, semana, horas, rol)
        asignacion.registrar_asignacion()
        self._guardar(self.gestor.asignaciones, asignacion, self.gestor.registrar_asignacion)

    def _listar_asignaciones(self):
        self._imprimir_lista(
            [f'{a.empleado.codigo} | {a.proyecto.codigo} | {a.semana} | '
             f'{a.horas_semanales}h | {a.rol} | {a.estado}'
             for a in self.gestor.asignaciones],
            'Sin asignaciones registradas.',
        )

    def _registrar_tarea(self):
        proyecto = self.gestor.buscar_proyecto(input('Código de proyecto: '))
        if proyecto is None:
            raise ValueError('Proyecto no encontrado.')
        empleado = self.gestor.buscar_empleado(input('Código de responsable: '))
        if empleado is None:
            raise ValueError('Empleado no encontrado.')
        tarea = Tarea(
            input('Código de tarea: '),
            input('Título: '),
            proyecto,
            empleado,
        )
        # ``Tarea.registrar_tarea`` valida la unicidad dentro del proyecto.
        tarea.registrar_tarea()
        self._guardar(self.gestor.tareas, tarea, self.gestor.registrar_tarea)

    def _listar_tareas(self):
        self._imprimir_lista(
            [f'{t.codigo} | {t.titulo} | {t.estado} | {t.proyecto.codigo}'
             for t in self.gestor.tareas],
            'Sin tareas registradas.',
        )

    def _actualizar_estado_tarea(self):
        codigo = input('Código de tarea: ')
        tarea = self.gestor.buscar_tarea(codigo)
        if tarea is None:
            raise ValueError(f'Tarea {codigo!r} no encontrada.')
        print('Estados válidos: Pendiente | En proceso | Finalizada')
        nuevo_estado = input('Nuevo estado: ').strip()
        tarea.actualizar_estado(nuevo_estado)
        self.gestor.guardar_datos()
        print('Estado actualizado.')

    def _registrar_horas(self):
        tarea = self.gestor.buscar_tarea(input('Código de tarea: '))
        if tarea is None:
            raise ValueError('Tarea no encontrada.')
        empleado = self.gestor.buscar_empleado(input('Código de empleado: '))
        if empleado is None:
            raise ValueError('Empleado no encontrado.')
        fecha = input('Fecha (YYYY-MM-DD): ')
        horas = input('Horas: ')
        registro = RegistroHoras(tarea, empleado, fecha, horas)
        # ``RegistroHoras.registrar_horas`` valida que la tarea exista en
        # el proyecto y que haya asignación activa del empleado esa semana.
        registro.registrar_horas()
        self._guardar(self.gestor.registros, registro, self.gestor.registrar_registro_horas)

    def _listar_registros(self):
        self._imprimir_lista(
            [f'{r.tarea.codigo} | {r.empleado.codigo} | {r.fecha} | {r.horas}h | '
             f'S/ {r.calcular_importe():.2f}'
             for r in self.gestor.registros],
            'Sin registros de horas.',
        )

    def _calcular_costo(self):
        proyecto = self.gestor.buscar_proyecto(input('Código de proyecto: '))
        if proyecto is None:
            raise ValueError('Proyecto no encontrado.')
        costo = CalculadoraCostos.calcular_costo_proyecto(proyecto)
        print(f'Costo total: S/ {costo:.2f}')

    def _calcular_saldo(self):
        proyecto = self.gestor.buscar_proyecto(input('Código de proyecto: '))
        if proyecto is None:
            raise ValueError('Proyecto no encontrado.')
        saldo = CalculadoraCostos.calcular_saldo(proyecto)
        print(f'Saldo: S/ {saldo:.2f}')

    def _comparar_presupuesto(self):
        proyecto = self.gestor.buscar_proyecto(input('Código de proyecto: '))
        if proyecto is None:
            raise ValueError('Proyecto no encontrado.')
        dentro = CalculadoraCostos.comparar_presupuesto(proyecto)
        print('Dentro del presupuesto.' if dentro else 'Presupuesto excedido.')

    def _guardar(self, coleccion, objeto, registrar):
        """Registra en memoria y persiste; si la escritura falla, revierte."""
        registrar(objeto)
        try:
            self.gestor.guardar_datos()
        except PersistenciaError:
            coleccion.remove(objeto)
            raise
        print('Registro guardado.')

    def _imprimir_lista(self, lineas, mensaje_vacio):
        """Imprime ``lineas`` o un mensaje si la lista está vacía (acepta iterable vacío)."""
        lista = list(lineas)
        if not lista:
            print(mensaje_vacio)
            return
        print('\n'.join(lista))