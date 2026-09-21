# Unidad 2: Procesamiento y representación de datos para IA

Trabajaremos con arreglos, tablas y tensores para preparar datos, comprobar sus
transformaciones y explorar sus características. Las notebooks servirán para
experimentar y explicar resultados; los módulos y las aplicaciones permitirán
repetir el procesamiento desde la terminal.

## Contenido

| Sesión | Tema | Contenido previsto | Estado |
|---|---|---|---|
| 1 | [Arreglos y representación con NumPy](./sesion-01-numpy/README.md) | `ndarray`, dimensiones, tipos, selección, vistas y copias. Dos proyectos ejecutables. | Disponible para revisión |
| 2 | [Vectorización y broadcasting](./sesion-02-vectorizacion/README.md) | Operaciones elemento a elemento, agregaciones, reshape, broadcasting y operaciones matriciales. Comparación con una implementación con ciclos. | Por desarrollar |
| 3 | [Manipulación y transformación con Pandas](./sesion-03-pandas/README.md) | Series, DataFrame, selección, filtros, orden, tipos y valores faltantes. | Por desarrollar |
| 4 | [Integración y calidad de datasets](./sesion-04-integracion-datasets/README.md) | Merge, join, concatenación, claves, duplicados y reporte de calidad. | Por desarrollar |
| 5 | [Almacenamiento e interoperabilidad tensorial](./sesion-05-almacenamiento-tensores/README.md) | CSV y Parquet; conversión NumPy–PyTorch, dimensiones, tipos y dispositivos. | Por desarrollar |
| 6 | [Exploración y visualización](./sesion-06-visualizacion/README.md) | Histogramas, dispersión, líneas y categorías con Matplotlib; interpretación de resultados. | Por desarrollar |

La secuencia puede ajustarse conforme avancemos. Las carpetas se numeran por
sesión dentro de la unidad; los prefijos de notebooks continúan como `u2_n1`,
`u2_n2`, etc., sin reiniciarse en cada sesión.

## Ejercicios

La [sesión 1](./sesion-01-numpy/README.md) contiene ejercicios en dos notebooks,
cada una dentro de su propio proyecto con `uv`, y una práctica integradora en
`PRACTICA.md`. Su README explica el orden de trabajo, la ubicación de los archivos
y los comandos para ejecutarlos.

Las sesiones posteriores indicarán del mismo modo dónde se resuelven sus ejercicios
conforme se incorporen sus materiales.

## Producto de la unidad

Construiremos gradualmente un procesamiento reproducible que reúna limpieza,
integración, almacenamiento, representación tensorial y visualización. En esta
primera sesión la evidencia es más pequeña: seleccionar mediciones, explicar sus
dimensiones y generar un resumen correcto sin modificar los datos originales.
