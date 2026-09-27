"""Demostración en memoria; no modifica archivos de datos."""
from gestion.modelos import (Cliente, Proyecto, Presupuesto, Desarrollador, QA,
                             LiderTecnico, Asignacion, Tarea, RegistroHoras, CalculadoraCostos)


def ejecutar_demo():
    cliente = Cliente('C001', 'Cliente académico', 'contacto@example.com')
    proyecto = Proyecto('P001', 'Sistema de ejemplo', cliente, Presupuesto(1000))
    empleados = [Desarrollador('E001', 'Ana', 'Python', 'Junior'),
                 QA('E002', 'Luis', 'Funcional', 'Manual'),
                 LiderTecnico('E003', 'Marta', 'Python', 2)]
    for indice, empleado in enumerate(empleados, start=1):
        Asignacion(empleado, proyecto, '2026-09-28', 16, type(empleado).__name__).registrar_asignacion()
        tarea = Tarea(f'T{indice:03}', f'Actividad {indice}', proyecto, empleado)
        tarea.registrar_tarea()
        registro = RegistroHoras(tarea, empleado, '2026-09-29', 2)
        registro.registrar_horas()
        print(f'{type(empleado).__name__}: S/ {registro.calcular_importe():.2f}')
    print(f'Costo total: S/ {CalculadoraCostos.calcular_costo_proyecto(proyecto):.2f}')
    print(f'Saldo: S/ {CalculadoraCostos.calcular_saldo(proyecto):.2f}')
    return proyecto


if __name__ == '__main__':
    ejecutar_demo()
