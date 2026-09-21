# Sesión 1: Arreglos y representación con NumPy

Una lista puede guardar mediciones; un arreglo permite expresar su organización
y operar sobre grupos de valores. Trabajaremos con temperaturas de tres salas
para construir selecciones correctas y llevar el análisis a una aplicación.

## Objetivos

- Interpretar `ndim`, `shape`, `size` y `dtype` a partir del significado de los datos.
- Seleccionar mediciones por posición y por condiciones, conservando las dimensiones necesarias.
- Distinguir una vista de una copia y evitar modificaciones accidentales.
- Reutilizar operaciones de NumPy en una notebook y en una aplicación ejecutada con `uv`.

Se retoman listas, slicing, funciones, módulos, archivos y los comandos de `uv`
de la unidad anterior.

## Contenido

| Orden | Material | Trabajo |
|---|---|---|
| 1 | [Guía de trabajo](./GUIA.md) | Preparar los proyectos y alternar terminal, notebook y editor |
| 2 | [Proyecto de exploración](./01-exploracion/README.md) | Arreglos, tipos, índices, máscaras y memoria compartida |
| 3 | [Proyecto de reporte](./02-reporte-mediciones/README.md) | Leer datos, seleccionar filas completas y resumir por sala |
| 4 | [Práctica](./PRACTICA.md) | Selección independiente y comprobación de resultados |
| 5 | [Ficha de datos](./datos/README.md) | Columnas, unidades, procedencia y valores no finitos |
| 6 | [Fuentes](./FUENTES.md) | Documentación oficial para consultar cada concepto |

## Estructura

```text
sesion-01-numpy/
├── datos/
│   ├── readings.csv
│   └── readings_quality.csv
├── 01-exploracion/
│   ├── main.py
│   ├── u2_n1_arreglos_numpy.ipynb
│   ├── pyproject.toml
│   └── uv.lock
└── 02-reporte-mediciones/
    ├── main.py
    ├── measurements/processing.py
    ├── tests/
    ├── u2_n2_reporte_mediciones.ipynb
    ├── pyproject.toml
    └── uv.lock
```

Los dos proyectos se ejecutan completos como referencia. Los ejercicios se
resuelven en las celdas reservadas o en un módulo nuevo, sin sustituir el código
necesario para continuar la sesión.

La primera notebook introduce los conceptos; la segunda conecta los resultados
con funciones reutilizables. Las reglas generales de broadcasting, `reshape`,
productos matriciales y mediciones de rendimiento se desarrollarán en la sesión 2.
