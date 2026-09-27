"""Menú ejecutable de los catálogos; el resto se integra progresivamente."""
from .datos import GestorDatos
from .modelos import Desarrollador, QA, LiderTecnico, Cliente, Proyecto, Presupuesto, Reporte


class MenuPrincipal:
    def __init__(self): self.opcion_actual = 0

    def mostrar_menu(self):
        print('\nGESTIÓN DE PROYECTOS — PRELIMINAR')
        print('1. Registrar empleado\n2. Listar empleados\n3. Buscar empleado y calcular tarifa')
        print('4. Registrar cliente\n5. Listar clientes\n6. Registrar proyecto\n7. Listar proyectos\n0. Salir')

    def solicitar_opcion(self):
        self.opcion_actual = int(input('Opción: '))
        return self.opcion_actual

    def mostrar_resultado(self, mensaje): print(mensaje)


class Sistema:
    def __init__(self, ruta_datos='datos/catalogos.json'):
        self.menu = MenuPrincipal()
        self.gestor = GestorDatos(ruta_datos)

    def iniciar(self):
        try:
            self.gestor.cargar_datos()
        except ValueError as error:
            print(error)
            return 1  # No abrir una sesión que podría sobrescribir datos ilegibles.
        while True:
            try:
                self.menu.mostrar_menu()
                opcion = self.menu.solicitar_opcion()
                if opcion == 0: return 0
                self.ejecutar_opcion(opcion)
            except (ValueError, OSError) as error:
                self.menu.mostrar_resultado(f'No se completó la operación: {error}')
            except (EOFError, KeyboardInterrupt):
                print('\nSesión finalizada. Los registros confirmados ya están guardados.')
                return 0

    def _guardar(self, coleccion, objeto, registrar):
        registrar(objeto)
        try:
            self.gestor.guardar_datos()
        except (OSError, ValueError):
            coleccion.remove(objeto)  # Revertir alta en memoria si falla la escritura.
            raise
        print('Registro guardado.')

    def ejecutar_opcion(self, opcion):
        if opcion == 1:
            tipo = input('Tipo (1 Desarrollador, 2 QA, 3 LiderTecnico): ').strip()
            if tipo not in ('1', '2', '3'): raise ValueError('Tipo de empleado inválido.')
            codigo, nombre = input('Código: '), input('Nombre: ')
            if tipo == '1': e = Desarrollador(codigo, nombre, input('Lenguaje: '), input('Nivel: '))
            elif tipo == '2': e = QA(codigo, nombre, input('Tipo de prueba: '), input('Herramienta: '))
            else: e = LiderTecnico(codigo, nombre, input('Tecnología: '), input('Cantidad a cargo: '))
            self._guardar(self.gestor.empleados, e, self.gestor.registrar_empleado)
        elif opcion == 2:
            print('\n'.join(Reporte(self.gestor).generar_reporte_empleados()) or 'Sin empleados.')
        elif opcion == 3:
            e = self.gestor.buscar_empleado(input('Código: '))
            if e is None: raise ValueError('Empleado no encontrado.')
            print(f'{e.nombre} | Importe: S/ {e.calcular_costo(input("Horas: ")):.2f}')
        elif opcion == 4:
            c = Cliente(input('Código: '), input('Razón social: '), input('Contacto ficticio: '))
            self._guardar(self.gestor.clientes, c, self.gestor.registrar_cliente)
        elif opcion == 5:
            print('\n'.join(c.mostrar_resumen() for c in self.gestor.clientes) or 'Sin clientes.')
        elif opcion == 6:
            c = self.gestor.buscar_cliente(input('Código de cliente existente: '))
            if c is None: raise ValueError('Cliente no encontrado.')
            p = Proyecto(input('Código de proyecto: '), input('Nombre: '), c,
                         Presupuesto(input('Presupuesto S/: ')))
            self._guardar(self.gestor.proyectos, p, self.gestor.registrar_proyecto)
        elif opcion == 7:
            print('\n'.join(Reporte(self.gestor).generar_reporte_proyectos()) or 'Sin proyectos.')
        else:
            raise ValueError('Seleccione una opción del menú.')
