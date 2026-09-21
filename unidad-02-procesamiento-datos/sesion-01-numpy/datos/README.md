# Mediciones de temperatura

Datos de ejemplo creados para esta lección. Se permite su copia, modificación y
redistribución mediante CC0 1.0: https://creativecommons.org/publicdomain/zero/1.0/.
No proceden de una instalación real.

Cada fila corresponde a una ronda de medición simultánea. Las tres columnas
representan `north_room`, `south_room` y `storage_room`, siempre en ese orden y
con temperatura en grados Celsius. La posición de la fila identifica la ronda;
no hay fechas ni intervalos de tiempo reales que interpretar.

| Archivo | Filas | Uso |
|---|---:|---|
| `readings.csv` | 8 | Selección de filas y columnas, vistas y resúmenes |
| `readings_quality.csv` | 4 | Dos filas completas y dos con valores no finitos |

`nan` representa una medición ausente; `inf` simula una lectura numérica no válida.
En el segundo proyecto se excluye la **fila completa** si contiene alguno de esos
valores, para comparar las salas usando las mismas rondas. No se imputan datos.
Esta regla es una decisión del ejercicio: la limpieza por columna y otras
políticas se discutirán al trabajar con Pandas.

Los archivos originales se conservan; las salidas se generan en `outputs/` dentro
del proyecto que las produce. Ser finito no garantiza que un valor sea físicamente
razonable: aquí no se implementan límites de operación de un sensor.
