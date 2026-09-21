# Exploración de arreglos

Explora dimensiones, tipos, selección y memoria compartida antes de resolver
los ejercicios de la notebook.

## Ejecutar

Desde esta carpeta:

```bash
uv sync --locked
uv run --locked python main.py
uv run --locked jupyter lab
```

Abre [u2_n1_arreglos_numpy.ipynb](./u2_n1_arreglos_numpy.ipynb). En VS Code,
selecciona el kernel de `.venv` después de sincronizar el proyecto.

Conserva la carpeta `../datos/` incluida en la sesión. El script resuelve su ruta
a partir de `main.py`; la notebook parte de la carpeta de este proyecto.

## Resultados

`main.py` informa las propiedades de la matriz: forma `(8, 3)`, 24 elementos y
192 bytes de datos en `float64`. `nbytes` describe el búfer numérico, no toda la
memoria del proceso.


[Guía de trabajo](../GUIA.md) · [Práctica](../PRACTICA.md) · [Ficha de datos](../datos/README.md)
