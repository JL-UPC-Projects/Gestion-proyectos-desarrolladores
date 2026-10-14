"""Menú principal: define y muestra las nueve opciones de la consola."""


class MenuPrincipal:
    """Cada opción es un entero; la clase solo muestra y captura (sin validar reglas de dominio)."""

    OPCION_EMPLEADOS = 1
    OPCION_CLIENTES = 2
    OPCION_PROYECTOS = 3
    OPCION_ASIGNACIONES = 4
    OPCION_TAREAS = 5
    OPCION_REGISTRO_HORAS = 6
    OPCION_COSTOS = 7
    OPCION_REPORTES = 8
    OPCION_SALIR = 0
    OPCION_REPORTES = 8

    OPCIONES_VALIDAS = (0,) + tuple(range(1, OPCION_REPORTES + 1))  # 0, 1..8

    def __init__(self):
        self.opcion_actual = 0

    def mostrar_menu(self):
        print('\nGESTIÓN DE PROYECTOS — Sistema académico FP2 (UPC)')
        print('1. Empleados')
        print('2. Clientes')
        print('3. Proyectos')
        print('4. Asignaciones')
        print('5. Tareas')
        print('6. Registro de horas')
        print('7. Costos y presupuestos')
        print('8. Reportes')
        print('0. Salir')

    def solicitar_opcion(self):
        """Lee la opción del usuario; lanza ``ValueError`` si no es entero o está fuera de 0..8."""
        texto = input('Opción: ').strip()
        try:
            opcion = int(texto)
        except ValueError as error:
            raise ValueError('Seleccione una opción del menú (0-8).') from error
        if opcion not in self.OPCIONES_VALIDAS:
            raise ValueError('Seleccione una opción del menú (0-8).')
        self.opcion_actual = opcion
        return opcion

    def mostrar_resultado(self, mensaje):
        print(mensaje)