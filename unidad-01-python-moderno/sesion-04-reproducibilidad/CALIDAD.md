# Calidad de código: pytest, Ruff, mypy y Makefile

Este bloque parte de la aplicación construida en la [guía](./GUIA.md).
Se puede realizar al cerrar la sesión o continuar en una sesión posterior.
El resultado es el mismo proyecto con comprobaciones automatizadas y comandos
compartidos por el equipo.

## 1. Agregar herramientas de desarrollo

Desde la carpeta de tu aplicación:

```bash
uv add --dev pytest ruff mypy
```

Observa `[dependency-groups].dev` en `pyproject.toml`. Las bibliotecas necesarias
para ejecutar la aplicación siguen en `[project].dependencies`. uv incluye el
grupo `dev` por defecto al sincronizar; para un entorno solo de ejecución se
puede usar `uv sync --locked --no-dev`.
[Grupos de dependencias](https://docs.astral.sh/uv/concepts/projects/dependencies/#dependency-groups).

## 2. Revisar formato y comportamiento

Copia las secciones `[tool.ruff]`, `[tool.ruff.lint]` y `[tool.pytest.ini_options]`
del [pyproject.toml de referencia](./proyecto/pyproject.toml) al tuyo.

Ruff revisa problemas como imports sin usar y puede dar formato. Agrega
`import math` a `processing.py` sin utilizarlo y ejecuta:

```bash
uv run ruff check .
uv run ruff check . --fix
uv run ruff format .
```

Lee el diagnóstico y observa el cambio antes de continuar. El lint no demuestra
que la media sea correcta. Para comprobar comportamiento, crea `tests/` y escribe
`test_report.py`:

```python
from pathlib import Path

import pytest

from readings.processing import summarize_file


def test_average(tmp_path: Path):
    path = tmp_path / "readings.jsonl"
    path.write_text(
        '{"station":"north","temperature":20}\n'
        '{"station":"south","temperature":24}\n',
        encoding="utf-8",
    )
    report = summarize_file(path)
    assert report.count == 2
    assert report.average_temperature == pytest.approx(22.0)
```

Ejecuta `uv run python -m pytest`. Cambia el valor esperado por `23.0`, observa
la prueba fallar y restáuralo. `tmp_path` proporciona una carpeta temporal aislada.
[Primeras pruebas con pytest](https://docs.pytest.org/en/stable/getting-started.html).

Amplía con archivo vacío, fila inválida y archivo inexistente. La referencia
incluye [pruebas de procesamiento](./proyecto/tests/test_processing.py) y
[pruebas de consola](./proyecto/tests/test_cli.py). `caplog` permite verificar
advertencias; ejecutar la aplicación como subproceso permite comprobar stdout,
stderr y códigos de salida. [Captura de logs](https://docs.pytest.org/en/stable/how-to/logging.html).

Mypy comprueba los tipos declarados en la aplicación sin ejecutarla. El comando
revisa `main.py` y los módulos de `readings`; `--strict` activa comprobaciones
adicionales. Ya usamos mypy en la sesión de anotaciones; aquí pasa a formar
parte de la revisión habitual del proyecto.

```bash
uv run --locked mypy --strict main.py readings
```

[Uso de mypy desde la terminal](https://mypy.readthedocs.io/en/stable/getting_started.html).

Antes de compartir:

```bash
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy --strict main.py readings
uv run --locked python -m pytest
```

`ruff format --check` comprueba sin modificar archivos.
[Tutorial de Ruff](https://docs.astral.sh/ruff/tutorial/).

## 3. Reunir comandos en un Makefile

Un Makefile asocia nombres de tareas con comandos. `make` ejecuta las
instrucciones que escribamos. Primero ejecuta cada
comando directamente para entenderlo.

Copia [Makefile](./proyecto/Makefile) en la raíz de tu proyecto. Sus recetas
empiezan con un carácter de tabulación real, no con espacios.

```makefile
.PHONY: check lint format-check types format test run sync

check: lint format-check types test

lint:
	uv run --locked ruff check .

format-check:
	uv run --locked ruff format --check .

types:
	uv run --locked mypy --strict main.py readings

format:
	uv run --locked ruff format .

test:
	uv run --locked python -m pytest

run:
	uv run --locked python main.py data/readings.jsonl

sync:
	uv sync --locked
```

Una regla tiene un objetivo, posibles prerrequisitos y una receta. `check` reúne
las cuatro comprobaciones; la primera regla también lo convierte en el objetivo
por defecto al escribir `make`. `.PHONY` indica tareas que deben ejecutarse aunque
exista un archivo llamado `test`, `run` o `check`.
[Manual oficial de GNU Make](https://www.gnu.org/software/make/manual/make.html).

```bash
make check
make run
```

`check` no modifica el código. `make format` sí lo reformatea y se ejecuta de
forma deliberada. Un comando que falla hace fallar la tarea; no ocultes ese
resultado con un prefijo `-` en la receta.

### Disponibilidad en el sistema

Comprueba `make --version`. En macOS puede estar disponible con las herramientas
de línea de comandos; en Linux se instala desde el gestor de paquetes de la
distribución. Windows no incluye GNU Make en PowerShell por defecto. Si ya
trabajas en WSL, ejecuta todo el proyecto en ese entorno. En PowerShell puedes
usar directamente los cuatro comandos `uv run --locked ...` del bloque anterior;
producen las mismas comprobaciones. Make no se instala mediante `uv add`.

## 4. Ejercicios de calidad

1. Agrega una prueba para una estación que contiene únicamente espacios. Debe
   rechazarse tras la normalización del modelo.
2. Agrega una prueba que compruebe el código de salida y la ausencia de reporte
   cuando el archivo no tiene lecturas válidas.
3. Introduce un import sin usar. Comprueba que `make check` falla; corrige el
   problema y vuelve a ejecutar la tarea.
4. Guarda los cambios en Git. En un clon nuevo ejecuta `uv sync --locked` y
   `make check` (o sus comandos directos).

La entrega incluye pruebas de éxito y fallo, configuración de herramientas,
Makefile, lockfile actualizado y comandos en el README. No se exige un porcentaje
de cobertura: las pruebas deben cubrir decisiones y errores importantes.
