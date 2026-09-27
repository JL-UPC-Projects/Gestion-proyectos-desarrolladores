"""Modelo preliminar del UML. Datos y tarifas exclusivamente académicos."""
from datetime import date
from math import isfinite


def texto(valor):
    valor = str(valor).strip()
    if not valor:
        raise ValueError('El campo no puede estar vacío.')
    return valor


def numero(valor, permitir_cero=False):
    valor = float(valor)
    if not isfinite(valor) or valor < 0 or (valor == 0 and not permitir_cero):
        raise ValueError('Ingrese un número válido mayor que cero.')
    return valor


class Empleado:
    def __init__(self, codigo, nombre):
        self.__codigo = texto(codigo)
        self.__nombre = texto(nombre)
        self.__capacidad_semanal = 48
        # Referencias compartidas, necesarias para consultar disponibilidad.
        self._asignaciones = []

    @property
    def codigo(self): return self.__codigo

    @property
    def nombre(self): return self.__nombre

    def calcular_costo(self, horas):
        raise NotImplementedError('Utilice Desarrollador, QA o LiderTecnico.')

    def horas_disponibles(self, semana):
        comprometidas = sum(a.horas_semanales for a in self._asignaciones
                            if a.semana == semana and a.estado == 'Activa')
        return self.__capacidad_semanal - comprometidas

    def verificar_disponibilidad(self, horas, semana):
        return numero(horas) <= self.horas_disponibles(semana)


class Desarrollador(Empleado):
    TARIFA_HORA = 60

    def __init__(self, codigo, nombre, lenguaje_principal, nivel):
        super().__init__(codigo, nombre)
        self.lenguaje_principal = texto(lenguaje_principal)
        self.nivel = texto(nivel)

    def calcular_costo(self, horas): return numero(horas) * self.TARIFA_HORA

    def aceptar_tarea(self, tarea): tarea.asignar_responsable(self)


class QA(Empleado):
    TARIFA_HORA = 50

    def __init__(self, codigo, nombre, tipo_prueba, herramienta):
        super().__init__(codigo, nombre)
        self.tipo_prueba = texto(tipo_prueba)
        self.herramienta = texto(herramienta)

    def calcular_costo(self, horas): return numero(horas) * self.TARIFA_HORA

    def registrar_prueba(self, tarea):
        raise NotImplementedError('Pendiente: definir resultados de pruebas con el equipo.')


class LiderTecnico(Empleado):
    TARIFA_HORA = 90

    def __init__(self, codigo, nombre, tecnologia_principal, equipo_a_cargo):
        super().__init__(codigo, nombre)
        self.tecnologia_principal = texto(tecnologia_principal)
        valor = numero(equipo_a_cargo, permitir_cero=True)
        if not valor.is_integer():
            raise ValueError('La cantidad de integrantes debe ser entera.')
        self.equipo_a_cargo = int(valor)

    def calcular_costo(self, horas): return numero(horas) * self.TARIFA_HORA

    def revisar_avance(self, proyecto): return proyecto.calcular_avance()


class Cliente:
    def __init__(self, codigo, razon_social, contacto):
        self.codigo = texto(codigo)
        self.razon_social = texto(razon_social)
        self.contacto = texto(contacto)

    def validar_datos(self):
        return all(str(v).strip() for v in (self.codigo, self.razon_social, self.contacto))

    def mostrar_resumen(self): return f'{self.codigo} | {self.razon_social} | {self.contacto}'


class Presupuesto:
    def __init__(self, monto_total):
        self.monto_total = numero(monto_total)
        self.monto_ejecutado = 0.0

    def actualizar_ejecucion(self, costo):
        # Recibe el total consolidado; no vuelve a sumar importes anteriores.
        self.monto_ejecutado = numero(costo, permitir_cero=True)

    def calcular_saldo(self): return self.monto_total - self.monto_ejecutado

    def verificar_exceso(self): return self.calcular_saldo() < 0


class Proyecto:
    def __init__(self, codigo, nombre, cliente, presupuesto):
        self.codigo = texto(codigo)
        self.nombre = texto(nombre)
        self.cliente = cliente
        self.presupuesto = presupuesto
        self.estado = 'Planificado'
        self.asignaciones = []
        self.tareas = []

    def registrar_proyecto(self):
        raise NotImplementedError('Registrar mediante GestorDatos.registrar_proyecto().')

    def consultar_personal_asignado(self):
        return list({a.empleado.codigo: a.empleado for a in self.asignaciones
                     if a.estado == 'Activa'}.values())

    def calcular_avance(self):
        if not self.tareas: return 0.0
        return 100 * sum(t.estado == 'Finalizada' for t in self.tareas) / len(self.tareas)


class Asignacion:
    def __init__(self, empleado, proyecto, semana, horas_semanales, rol):
        # La semana se identifica por su lunes, en formato YYYY-MM-DD.
        inicio = date.fromisoformat(semana)
        if inicio.weekday() != 0:
            raise ValueError('La semana debe identificarse por la fecha de su lunes.')
        self.empleado = empleado
        self.proyecto = proyecto
        self.semana = inicio.isoformat()
        self.horas_semanales = numero(horas_semanales)
        self.rol = texto(rol)
        self.estado = 'Pendiente'

    def validar_disponibilidad(self):
        return self.empleado.verificar_disponibilidad(self.horas_semanales, self.semana)

    def registrar_asignacion(self):
        if self.estado != 'Pendiente':
            raise ValueError('Esta asignación ya fue registrada.')
        if any(a.proyecto.codigo == self.proyecto.codigo and a.semana == self.semana
               and a.estado == 'Activa' for a in self.empleado._asignaciones):
            raise ValueError('Ya existe una asignación activa para ese proyecto y semana.')
        if not self.validar_disponibilidad():
            raise ValueError('La asignación supera las 48 horas semanales.')
        self.estado = 'Activa'
        self.empleado._asignaciones.append(self)
        self.proyecto.asignaciones.append(self)

    def modificar_horas(self, horas):
        horas = numero(horas)
        if self.estado != 'Activa': raise ValueError('La asignación no está activa.')
        if horas > self.empleado.horas_disponibles(self.semana) + self.horas_semanales:
            raise ValueError('La asignación supera las 48 horas semanales.')
        self.horas_semanales = horas

    def finalizar_asignacion(self): self.estado = 'Finalizada'


class Tarea:
    def __init__(self, codigo, titulo, proyecto, responsable):
        self.codigo = texto(codigo)
        self.titulo = texto(titulo)
        self.proyecto = proyecto
        self.estado = 'Pendiente'
        self.registros = []
        self.asignar_responsable(responsable)

    def registrar_tarea(self):
        if any(t.codigo == self.codigo for t in self.proyecto.tareas):
            raise ValueError('Código de tarea duplicado en el proyecto.')
        self.proyecto.tareas.append(self)

    def asignar_responsable(self, e):
        if e not in self.proyecto.consultar_personal_asignado():
            raise ValueError('El responsable debe estar asignado al proyecto.')
        self.responsable = e

    def actualizar_estado(self, estado):
        if estado not in ('Pendiente', 'En proceso', 'Finalizada'):
            raise ValueError('Estado de tarea inválido.')
        self.estado = estado


class RegistroHoras:
    def __init__(self, tarea, empleado, fecha, horas):
        self.tarea = tarea
        self.empleado = empleado
        self.fecha = date.fromisoformat(fecha).isoformat()
        self.horas = numero(horas)

    def validar_registro(self):
        fecha = date.fromisoformat(self.fecha)
        return any(a.proyecto is self.tarea.proyecto and a.estado == 'Activa'
                   and 0 <= (fecha - date.fromisoformat(a.semana)).days < 7
                   for a in self.empleado._asignaciones)

    def registrar_horas(self):
        if self.tarea not in self.tarea.proyecto.tareas:
            raise ValueError('La tarea no está registrada.')
        if self in self.tarea.registros: raise ValueError('Registro ya agregado.')
        if not self.validar_registro():
            raise ValueError('El empleado debe tener asignación activa en esa semana.')
        self.tarea.registros.append(self)

    def calcular_importe(self): return self.empleado.calcular_costo(self.horas)


class CalculadoraCostos:
    @staticmethod
    def calcular_costo_proyecto(p):
        costo = sum(r.calcular_importe() for t in p.tareas for r in t.registros)
        p.presupuesto.actualizar_ejecucion(costo)
        return costo

    @staticmethod
    def calcular_saldo(p):
        CalculadoraCostos.calcular_costo_proyecto(p)
        return p.presupuesto.calcular_saldo()

    @staticmethod
    def comparar_presupuesto(p): return CalculadoraCostos.calcular_saldo(p) >= 0


class Reporte:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fecha_emision = date.today().isoformat()

    def generar_reporte_proyectos(self):
        return [f'{p.codigo} | {p.nombre} | {p.estado}' for p in self.gestor.proyectos]

    def generar_reporte_empleados(self):
        return [f'{e.codigo} | {e.nombre} | {type(e).__name__}' for e in self.gestor.empleados]

    def generar_reporte_tareas(self):
        return [f'{t.codigo} | {t.titulo} | {t.estado}'
                for p in self.gestor.proyectos for t in p.tareas]

    def generar_reporte_costos(self):
        return [f'{p.codigo} | saldo: S/ {CalculadoraCostos.calcular_saldo(p):.2f}'
                for p in self.gestor.proyectos]
