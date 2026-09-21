# Reporte de mediciones

Genera un reporte de temperaturas reutilizando las mismas funciones desde
la terminal y desde la notebook.

## Ejecutar

Desde esta carpeta:

```bash
uv sync --locked
uv run --locked python main.py
uv run --locked jupyter lab
```

Abre [u2_n2_reporte_mediciones.ipynb](./u2_n2_reporte_mediciones.ipynb). En VS Code,
selecciona el kernel de `.venv` después de sincronizar el proyecto.

Conserva la carpeta `../datos/` incluida en la sesión. El script resuelve su ruta
a partir de `main.py`; la notebook parte de la carpeta de este proyecto.

## Aplicación

```bash
uv run --locked python main.py ../datos/readings_quality.csv --output-dir outputs/quality
uv run --locked python -m pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

`main.py` coordina la entrada y las salidas; `measurements/processing.py` contiene
las operaciones; `tests/` comprueba las medias, las dimensiones, el filtrado y la
ejecución de la aplicación.

La entrada predeterminada usa ocho rondas y tres salas, con medias `25.5`, `27.5`
y `23.5`. La entrada con errores usa dos rondas y rechaza otras dos.

Los resultados se guardan en `outputs/report.json` y
`outputs/complete_readings.npy`, y se reemplazan al repetir la ejecución.
`--output-dir` permite conservar cada resultado en una carpeta diferente.
Los errores de lectura o de validación producen un mensaje en stderr y código de
salida 1. Se rechazan encabezados incorrectos, matrices vacías y entradas sin
ninguna fila completa. Los valores no finitos se filtran por fila completa.


[Guía de trabajo](../GUIA.md) · [Práctica](../PRACTICA.md) · [Ficha de datos](../datos/README.md)
