# Alcance y continuación del preliminar

Esta implementación es una base de trabajo, no evidencia de que todos los requisitos del informe estén terminados. Se conserva un diseño simple: biblioteca estándar, consola, listas, clases y archivos JSON.

## Correspondencia con el diseño

Las 15 clases están declaradas: Sistema, MenuPrincipal, GestorDatos, Empleado, Desarrollador, QA, LiderTecnico, Cliente, Proyecto, Presupuesto, Asignacion, Tarea, RegistroHoras, CalculadoraCostos y Reporte.

Diferencias que deben revisarse y reflejarse en el UML final:

- Se agregan listas de referencias en Empleado, Proyecto y Tarea para implementar disponibilidad, avance y acumulación de costos. No se duplican los objetos referenciados.
- Reporte recibe un GestorDatos para consultar sus colecciones.
- La persistencia inicial usa un único snapshot `catalogos.json`. Los seis archivos y las colecciones de movimientos previstos en el informe siguen pendientes.
- El menú inicial agrupa operaciones de catálogos; aún no corresponde al menú completo de nueve opciones del informe.
- `QA.registrar_prueba` está pendiente de definición. `Proyecto.registrar_proyecto` dirige explícitamente al servicio de registro de GestorDatos.
- El encapsulamiento completo, los contratos finales de retorno y la unicidad global de tareas deben cerrarse en la siguiente iteración.

## Reglas implementadas en memoria

- La semana se identifica mediante la fecha de su lunes (`YYYY-MM-DD`).
- Se suman asignaciones activas en la misma semana, entre todos los proyectos; no se permiten más de 48 horas.
- No se admite una segunda asignación activa del mismo empleado/proyecto/semana.
- El responsable de una tarea debe estar asignado al proyecto.
- Registrar horas requiere una tarea registrada y una asignación activa del empleado en la semana de la fecha indicada.
- Las horas comprometidas controlan disponibilidad; las horas efectivas determinan costos.
- Cada registro calcula su importe polimórficamente. El costo se consolida desde las tareas y no se duplica al consultar varias veces.

## Límites conocidos

La validación de horas no impone un máximo diario ni limita el acumulado de horas efectivas al comprometido: debe acordarse esa regla antes de ampliarla. Los importes usan `float` por simplicidad académica; si se requiere exactitud monetaria contable, migrar a Decimal. No se admite edición concurrente del archivo por varios procesos. La demo trabaja en memoria y no guarda movimientos.

## Próximas iteraciones propuestas

1. Revisar el preliminar en equipo y ajustar UML, responsabilidades de registro y encapsulamiento.
2. Completar persistencia de asignaciones, tareas y horas con identificadores; validar referencias y estados al cargar.
3. Incorporar los módulos pendientes al menú, con búsquedas, consultas y mensajes de validación.
4. Completar reportes y estados; verificar presupuesto excedido y disponibilidad entre proyectos.
5. Ejecutar la matriz de aceptación del informe, corregir errores y preparar capturas y ZIP para la semana 7.

## Distribución propuesta según el informe

| Integrante | Continuación sugerida |
| --- | --- |
| Jose Luis Pintado Vasquez | Sistema, MenuPrincipal, GestorDatos, integración e informe |
| Bryan Paul Villagomez Sobero | Empleado, Desarrollador, QA, LiderTecnico y tarifas |
| Fabiola Ivette Valverde Miranda | Cliente, Proyecto, Presupuesto, Asignacion y capacidad |
| Osmar Luigi Mosquera Quispe | Tarea, RegistroHoras, CalculadoraCostos y Reporte |

La tabla expresa responsabilidades previstas, no aportes realizados. Cada integrante debe revisar y comprender su módulo, desarrollar sus cambios y registrar sus propios commits reales.

## Verificación del preliminar

Se ejecutó `python -m unittest discover -s tests -v`: 13 pruebas satisfactorias. Se ejecutó `python demo.py`: costo S/ 400 y saldo S/ 600. Quedan pendientes las pruebas de aceptación de la aplicación final y las capturas del equipo.
