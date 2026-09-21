# Guía de trabajo

## 1. Preparar el proyecto de exploración

Desde la raíz del repositorio:

```bash
cd unidad-02-procesamiento-datos/sesion-01-numpy/01-exploracion
uv sync --locked
uv run --locked python main.py
uv run --locked jupyter lab
```

Abre `u2_n1_arreglos_numpy.ipynb` en JupyterLab. El kernel ejecuta Python y mantiene
las variables de las celdas; reiniciarlo borra ese estado. Al ejecutar Jupyter desde
el proyecto con `uv`, se usa su entorno y sus dependencias.

En VS Code, abre la carpeta del proyecto, ejecuta `uv sync --locked` en su terminal
y selecciona **Select Kernel → Python Environments → .venv**. En macOS/Linux el
intérprete está en `.venv/bin/python`; en Windows, en `.venv/Scripts/python.exe`.
La primera celda muestra el intérprete y el directorio para comprobar la selección.

Los comandos de `uv` se escriben en la terminal. Para cambiar dependencias, utiliza
`uv add` allí y reinicia el kernel. No hace falta instalar NumPy desde una celda.

El script muestra `Shape: (8, 3)`, dos dimensiones y 24 elementos. Primero explica
qué significan 8 y 3; después recorre la notebook hasta la selección por columnas.

## 2. Recuperar cómo se crea el entorno

Los proyectos de referencia ya incluyen sus archivos de configuración. Para
reconstruir un proyecto de exploración **en otra carpeta nueva**, ejecuta:

```bash
uv init --no-package --python 3.13 numpy-lab
cd numpy-lab
uv add numpy
uv add --dev jupyterlab ipykernel nbconvert
uv run jupyter lab
```

`numpy` es una dependencia de la aplicación. JupyterLab e ipykernel permiten el
trabajo interactivo; nbconvert permite ejecutar la notebook desde la terminal.
`uv.lock` registra las versiones resueltas. Un proyecto creado hoy puede resolver
versiones distintas de la referencia; `uv sync --locked` reproduce las de cada lock.

## 3. Experimentar con selecciones y copias

Antes de ejecutar cada ejemplo, anticipa el valor y su forma. Compara una selección
`readings[:, 0]` con `readings[:, 0:1]`. Después modifica una vista creada desde una
copia de trabajo y observa el arreglo que comparte su memoria.

Resuelve los ejercicios 1 a 6 de la primera notebook. El archivo original y la
variable base se conservan para que los experimentos no alteren los resultados
posteriores. No basta con que una expresión se ejecute: justifica qué sala o ronda
representa cada posición.

## 4. Pasar al proyecto de reporte

Detén JupyterLab con Ctrl+C en la terminal y confirma su cierre si lo solicita.
Desde `01-exploracion`:

```bash
cd ../02-reporte-mediciones
uv sync --locked
uv run --locked python main.py
uv run --locked python main.py ../datos/readings_quality.csv --output-dir outputs/quality
uv run --locked jupyter lab
```

Abre `u2_n2_reporte_mediciones.ipynb`. Recorre las funciones de
`measurements/processing.py`: lectura, comprobación de forma, selección y resumen.
La notebook importa esas funciones. `main.py` añade argumentos, logging y archivos
de salida. Si editas un módulo, reinicia el kernel antes de repetir la notebook,
para evitar usar una importación anterior.

El CSV se carga como una matriz de números; el encabezado se valida por separado.
Pandas y sus etiquetas de columnas se introducirán más adelante. El arreglo no
conserva por sí mismo los nombres de las salas.

## 5. Revisar los resultados

Con `readings.csv` se usan las ocho filas. Las medias por sala son `25.5`, `27.5`
y `23.5` °C. Con `readings_quality.csv` se usan dos filas y se rechazan dos; las
medias son `23.0`, `25.0` y `21.0` °C.

La aplicación produce `report.json` y `complete_readings.npy`. El formato `.npy`
conserva la forma y el tipo del arreglo; los nombres y las unidades se describen
en la ficha de datos. Ejecutar de nuevo con la misma carpeta de salida reemplaza
estos dos archivos. Usa `--output-dir` para conservar resultados separados.

Los mensajes operativos van a stderr y el reporte JSON a stdout, retomando la
separación estudiada con logging.

## 6. Comprobar y resolver la práctica

Desde el proyecto de reporte:

```bash
uv run --locked python -m pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

También puedes usar `make check` si tienes Make instalado. Estos comandos retoman
las herramientas de calidad de la unidad 1. A continuación resuelve la
[práctica](./PRACTICA.md).

Para comprobar cada notebook desde la carpeta de su proyecto:

```bash
uv run --locked jupyter nbconvert --to notebook --execute u2_n1_arreglos_numpy.ipynb --output u2_n1_arreglos_numpy.executed.ipynb
```

En el segundo proyecto cambia el nombre por `u2_n2_reporte_mediciones.ipynb` y la
salida por `u2_n2_reporte_mediciones.executed.ipynb`. Los archivos ejecutados quedan
ignorados por Git. En JupyterLab, la comprobación equivalente es reiniciar el
kernel y ejecutar todas las celdas.
