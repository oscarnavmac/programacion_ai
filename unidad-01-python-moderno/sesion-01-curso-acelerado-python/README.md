# Sesión 1: Curso acelerado de Python

Taller gradual para establecer una base común de Python, sin presuponer experiencia
en programación. El material puede continuar en la siguiente sesión según el ritmo
del grupo; la prioridad es resolver y explicar los ejercicios.

## Presentación de apertura

Antes de la notebook 1, revisaremos la asignatura, las tres unidades del curso,
la evaluación, los materiales y una introducción a Python y su uso en IA.

- [Presentación de introducción (PDF)](https://drive.google.com/file/d/18klbYcjpSpyDiwToHvbNQFEvy699FbK-/view?usp=drivesdk)

## Notebooks

| Notebook | Archivo en el repositorio | Google Colab |
|---|---|---|
| 1. Curso acelerado de Python para IA | [Ver notebook](./u1_n1_curso_acelerado_python.ipynb) | [![Abrir en Google Colab](https://img.shields.io/badge/Abrir_en-Google_Colab-F9AB00?logo=googlecolab&logoColor=F9AB00&labelColor=333333)](https://colab.research.google.com/drive/1Q4dLL8eTF55DsSLiOXE2frOw3iFhuHkL) |
| 2. El Zen de Python, con ejemplos | [Ver notebook](./u1_n2_zen_de_python.ipynb) | [![Abrir en Google Colab](https://img.shields.io/badge/Abrir_en-Google_Colab-F9AB00?logo=googlecolab&logoColor=F9AB00&labelColor=333333)](https://colab.research.google.com/drive/1MTMMN5ifsWDA2aLzHCqRdMRmhp51K0jM) |

El orden es intencional: la segunda notebook utiliza los conceptos de la primera
para discutir legibilidad, simplicidad y manejo explícito de errores.

Ambas notebooks se ejecutan en Colab y sólo utilizan la biblioteca estándar.
Durante esta sesión no es necesario preparar un entorno local.
Las explicaciones están en español en ambas notebooks. En la primera, el código
puede estar en español; a partir de la segunda, los nombres, comentarios y mensajes
del código están en inglés.

## Temas del curso acelerado

- Valores, cadenas, sintaxis y primeros pasos para principiantes.
- Listas, slicing, tuplas, desempaquetado, diccionarios y conjuntos.
- Mutabilidad, alias y copias de estructuras anidadas.
- Decisiones, ciclos, comprehensions y distinción entre cero y ausencia.
- Funciones, ordenamiento por criterio, conteo y agrupación.
- Excepciones y comprobaciones con `assert`.
- POO: clases, instancias, atributos, métodos y estado independiente.
- Caso integrador: conservar predicciones y resumir un lote.

## Dinámica del taller

La primera notebook incluye 11 ejercicios con la secuencia **predecir, ejecutar,
explicar y modificar**. Las celdas de ejercicios quedan abiertas; los ejemplos,
laboratorios y actividades de exploración se ejecutan sin completarlas.

Cada ejercicio se entrega resuelto en la celda correspondiente, junto con las
predicciones, explicaciones y comprobaciones solicitadas.

Para recorrer cada notebook, ejecuta las celdas desde arriba. En el laboratorio de
errores, descomenta una línea a la vez y vuelve a comentarla después de analizarla
para que **Ejecutar todo** pueda terminar.

Puede pausarse al terminar los primeros pasos, el taller de datos o el tramo de POO.
El último ejercicio comprueba con `assert` el contrato del caso integrador y sus
casos límite. La segunda notebook conserva su recorrido independiente por las 19
reglas del Zen.

## Temas del Zen

La segunda notebook desarrolla las **19 reglas**, cada una con su título y una
explicación en español. Los comentarios de los ejemplos identifican qué versión
sigue la regla y cuál es el contraejemplo, con una breve justificación.

- Belleza, explicitud, simplicidad y legibilidad.
- Complejidad, anidación y densidad del código.
- Consistencia, practicidad y manejo de errores.
- Ambigüedad y convenciones del lenguaje.
- Cuándo actuar, cuándo esperar y cómo explicar una implementación.
- Espacios de nombres y procedencia de las funciones.
- Reto de refactorización que conserva el comportamiento y comprueba casos límite.
