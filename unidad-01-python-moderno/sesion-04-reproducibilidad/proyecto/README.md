# Reporte de lecturas

Aplicación de consola que lee un archivo JSON Lines, valida cada registro y
calcula la temperatura media. Omite registros inválidos con una advertencia.
Un archivo sin lecturas válidas o que no se puede leer produce una salida de error.

Desde esta carpeta:

```bash
uv sync --locked
uv run --locked python main.py data/readings.jsonl
uv run --locked python main.py data/readings.jsonl --log-level DEBUG --log-file logs/app.log
```

El resultado JSON se escribe en stdout y los logs de consola en stderr.
La muestra contiene tres lecturas válidas, una rechazada y una media de 22.0.

```bash
uv run --locked python main.py data/readings.jsonl > report.json
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

Códigos de salida: `0` si se genera el reporte, `1` si falla la lectura o no hay
registros válidos, `2` si los argumentos no son válidos. Una fila rechazada no
hace fallar un reporte que tiene otras lecturas válidas.

Las rutas de entrada y de logs se interpretan respecto del directorio de trabajo.
Para llamar al script desde otra carpeta, proporciona rutas absolutas.
El modelo acepta conversiones numéricas de Pydantic; no utiliza validación estricta.
Las líneas vacías cuentan como registros rechazados.

Consulta la [guía de construcción](../GUIA.md) para crear la aplicación paso a paso.

El bloque final de [calidad de código](../CALIDAD.md) reúne estas comprobaciones
en `make check`. El Makefile también incluye `make run`, `make sync` y
`make format`; este último modifica el formato del código.
