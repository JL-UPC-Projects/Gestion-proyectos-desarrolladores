# Gestión de proyectos y asignación de desarrolladores

Proyecto académico de Fundamentos de Programación 2 — UPC. Caso de simulación inspirado en una consultora de software; utiliza datos ficticios y tarifas académicas.

## Estado: preliminar ejecutable

Según la indicación del docente, el trabajo parcial (aproximadamente semana 4) presenta el diseño. En la semana 7 se presenta el sistema funcionando, con las mejoras necesarias. Esta base permite empezar a implementar y contrastar el UML; **no constituye la entrega final**.

Requiere Python 3.10 o superior. No necesita librerías externas.

```bash
python main.py
```

En macOS puede utilizarse `python3` en lugar de `python`.

## Qué funciona

- Menú de consola: registrar/listar empleados, clientes y proyectos; buscar empleado y calcular su importe.
- Tres categorías con herencia y polimorfismo: Desarrollador (S/ 60/h), QA (S/ 50/h), LiderTecnico (S/ 90/h).
- Catálogos guardados en `datos/catalogos.json`, con reconstrucción de la relación proyecto–cliente al reiniciar.
- Validación de campos, duplicados, importes no finitos, clientes inexistentes y opciones inválidas.
- Protección del archivo original ante JSON inválido; escritura mediante archivo temporal y reemplazo.
- Modelo en memoria: asignaciones por semana, máximo de 48 horas, tareas, horas efectivas, presupuesto y reportes.

Para ver el flujo del modelo sin modificar datos:

```bash
python demo.py
```

Resultado esperado: Desarrollador S/ 120, QA S/ 100, líder técnico S/ 180; total S/ 400 y saldo S/ 600 sobre un presupuesto de S/ 1 000.

Para ejecutar las pruebas:

```bash
python -m unittest discover -s tests -v
```

## Estructura

```text
main.py                 Entrada del menú
 demo.py                Ejemplo de operaciones en memoria
 gestion/modelos.py     12 clases de negocio del UML
 gestion/datos.py       GestorDatos
 gestion/sistema.py     Sistema y MenuPrincipal
 tests/                 Pruebas automatizadas
 docs/                  Alcance y plan de continuación
```

## Uso rápido

1. Ejecutar `python main.py`.
2. Registrar un empleado con opción 1; consultarlo con 2 o 3.
3. Registrar un cliente con opción 4.
4. Registrar un proyecto con opción 6 usando el código del cliente.
5. Salir con 0 y volver a ejecutar: los catálogos se recuperan.

Se puede usar otro archivo con `python main.py --datos ruta/catalogos.json`. Los datos locales están excluidos de Git. No ingresar información real de NTT DATA ni de clientes.

## Pendiente para la semana 7

- Integrar asignaciones, tareas, horas y reportes al menú; permitir búsqueda y consulta completas.
- Persistir los movimientos y estados. La versión actual **solo guarda catálogos**; rechaza el guardado de proyectos con movimientos para evitar pérdida silenciosa.
- Acordar el comportamiento de `QA.registrar_prueba`. Por ahora lanza `NotImplementedError` explícitamente.
- Resolver la responsabilidad de `Proyecto.registrar_proyecto`: el alta se realiza hoy en `GestorDatos`.
- Centralizar códigos de tareas únicos en todo el sistema (hoy se verifican por proyecto).
- Completar encapsulamiento y la separación de archivos por clase si así lo acuerda el grupo.
- Sincronizar UML, informe y código; ejecutar los casos de aceptación y adjuntar evidencias reales.

Consultar [plan y diferencias respecto al UML](docs/PRELIMINAR.md). Las pruebas automatizadas de esta base no sustituyen las evidencias del sistema final.
