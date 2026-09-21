# De una carpeta a una aplicación reproducible

La aplicación de esta sesión recibe un archivo con lecturas de temperatura,
valida sus registros y produce un reporte. Los registros inválidos se cuentan y
se omiten; si no hay ninguno válido, el programa termina con un error.

## 1. Preparar la terminal

Una terminal ejecuta comandos en un **directorio de trabajo**. Abre una carpeta
de prácticas en tu editor y su terminal integrada. `cd nombre` entra en una
carpeta; `cd ..` vuelve a la anterior. En macOS/Linux, `pwd` muestra dónde estás
y `ls` lista los archivos; en PowerShell puedes usar `Get-Location` y `Get-ChildItem`.

Instala `uv` siguiendo las [instrucciones de Astral](https://docs.astral.sh/uv/getting-started/installation/).
El instalador independiente es una opción para macOS/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

En Windows, desde PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Abre una nueva terminal si el comando todavía no aparece y comprueba:

```bash
uv --version
uv python install 3.13
```

`uv` gestiona intérpretes, entornos y dependencias. Python es quien ejecuta el
programa. Un entorno virtual permite que distintos proyectos utilicen distintas
versiones de sus bibliotecas.

## 2. Crear el proyecto

En una carpeta de prácticas, fuera de la carpeta `proyecto` de esta referencia:

```bash
uv init --no-package --python 3.13 --vcs none readings-report
cd readings-report
uv run python main.py
```

`--no-package` crea una aplicación ejecutada como script. Desde uv 0.12, el
comportamiento por defecto de `uv init` es crear una aplicación empaquetada con
`src/`; por eso aquí explicitamos la opción. `--vcs none` pospone la creación del
repositorio Git hasta conocer qué archivos debemos guardar.
[Creación de proyectos](https://docs.astral.sh/uv/concepts/projects/init/).

Identifica `main.py`, `pyproject.toml`, `.python-version` y `README.md`.
Después de ejecutar el programa también encontrarás `.venv/` y `uv.lock`.

| Elemento | Función |
|---|---|
| `main.py` | Entrada de nuestra aplicación. |
| `pyproject.toml` | Metadatos, requisitos y configuración de herramientas. |
| `.python-version` | Selección local del intérprete para uv. |
| `uv.lock` | Resolución de dependencias, con versiones y artefactos. |
| `.venv/` | Entorno local que se puede reconstruir. |
| `README.md` | Instrucciones para usar y comprobar el proyecto. |

`uv run` prepara el entorno del proyecto antes de ejecutar el comando. No es
necesario activar `.venv` manualmente en este recorrido.
[Trabajo con proyectos](https://docs.astral.sh/uv/guides/projects/).

**Comprobación:** ejecuta `uv run python -c "import sys; print(sys.executable)"`.
La ruta debe corresponder al entorno del proyecto.

## 3. Entender main.py

Sustituye el contenido inicial por:

```python
def main() -> int:
    print("Reading report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Ejecuta `uv run python main.py` y después `uv run python -c "import main"`.
La primera instrucción imprime el mensaje; la segunda no.

`main.py` es una convención de nombre. Python no busca ni llama automáticamente
una función llamada `main`. La condición comprueba si el archivo se está ejecutando
como entrada del programa; al importarlo, su nombre de módulo es `main`.
`SystemExit` convierte el retorno en un código de salida: `0` representa éxito.
[Entorno de ejecución principal](https://docs.python.org/3/library/__main__.html).

Un programa nuevo arranca en un proceso nuevo: no conserva variables de una
notebook ni resultados de una ejecución anterior. Las entradas deben llegar
por argumentos, archivos u otra interfaz definida.

## 4. Declarar dependencias

```bash
uv add "pydantic>=2,<3"
```

Pydantic será una dependencia de ejecución. `logging`, `argparse` y `pathlib` pertenecen a la biblioteca estándar:
no se agregan como dependencias externas.

Abre `pyproject.toml`. Conserva las dependencias que escribió uv y cambia
`requires-python` a `">=3.12"`, la compatibilidad mínima de esta aplicación.
`.python-version` puede seguir seleccionando `3.13`. Son decisiones distintas:
compatibilidad declarada y versión elegida para trabajar.

```bash
uv lock
uv sync
uv tree
```

`uv tree` permite identificar dependencias directas y transitivas: algunas
bibliotecas son necesarias porque otra biblioteca depende de ellas.
[Dependencias y grupos](https://docs.astral.sh/uv/concepts/projects/dependencies/).

**Comprobación:** localiza Pydantic en `[project].dependencies`. Compara esa declaración con las versiones resueltas
en `uv.lock`; no edites el lockfile a mano.

## 5. Separar responsabilidades

La estructura final de esta aplicación será:

```text
readings-report/
├── main.py
├── readings/
│   ├── __init__.py
│   ├── models.py
│   ├── processing.py
│   └── logging_config.py
├── data/
│   ├── readings.jsonl
│   └── invalid.jsonl
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

Un archivo `.py` es un módulo. La carpeta `readings`, con `__init__.py`, es un
paquete importable que agrupa módulos. Esto no significa que hayamos construido
una distribución instalable ni publicado una biblioteca.

| Archivo | Responsabilidad |
|---|---|
| `models.py` | Definir qué datos acepta una lectura y cómo se representa el reporte. |
| `processing.py` | Leer, validar, acumular y devolver un resultado. |
| `logging_config.py` | Elegir destinos, niveles y formato de los logs. |
| `main.py` | Interpretar argumentos, configurar la ejecución y presentar el resultado. |

Crea las carpetas y un `readings/__init__.py` vacío. Usa nombres que describan el
problema; evita llamar a un archivo `logging.py`, `json.py` o `pydantic.py`, porque
podría ocultar el módulo que intentas importar.

### Modelos y datos

Crea `readings/models.py` con el contenido de [models.py](./proyecto/readings/models.py).
`Reading` exige una estación no vacía y una temperatura finita. `Report` representa
la salida. Se retoma Pydantic de la sesión 2 sin añadir otra biblioteca de datos.
[Restricciones de campos](https://docs.pydantic.dev/latest/concepts/fields/).

Crea `data/readings.jsonl` copiando la [muestra](./proyecto/data/readings.jsonl).
Cada línea es un objeto JSON independiente; el archivo completo no es una lista JSON.
La tercera línea tiene una temperatura inválida. Crea también
[data/invalid.jsonl](./proyecto/data/invalid.jsonl), donde todas las lecturas fallan.

### Procesamiento

Crea `readings/processing.py` a partir de [processing.py](./proyecto/readings/processing.py).
Lee primero la función ignorando temporalmente las llamadas `logger.*`:
abre el archivo con `with`, valida cada línea, acumula una media y devuelve `Report`.
La media se actualiza sin guardar todas las lecturas.

Los errores de validación permiten continuar con otra fila. Los errores que
impiden leer el archivo se propagan al llamador. No se devuelve un reporte de
éxito si ninguna fila fue válida. Las líneas vacías también se rechazan.

Sustituye temporalmente `main.py` por:

```python
from pathlib import Path

from readings.processing import summarize_file


def main() -> int:
    report = summarize_file(Path("data/readings.jsonl"))
    print(report.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Ejecuta `uv run python main.py`. Verás un reporte con `count=3`, `rejected=1` y
`average_temperature=22.0`. También puede aparecer la advertencia del registro
rechazado: logging tiene un mecanismo de respaldo para avisos aunque todavía no
hayamos configurado los destinos.

## 6. Incorporar logging

El resultado del programa y los eventos de su ejecución tienen propósitos
diferentes. El reporte se imprime para consumirlo; los logs ayudan a entender
qué ocurrió mientras se produjo.

En la parte superior de `main.py`, agrega `import logging`. Como primera
instrucción dentro de `main()`, antes de procesar el archivo, agrega:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)
```

En `processing.py`, `logging.getLogger(__name__)` crea o recupera el logger del
módulo. La configuración se hace en la entrada de la aplicación, una sola vez;
los módulos se limitan a emitir eventos.
[Guía de logging](https://docs.python.org/3/howto/logging.html).

| Nivel | Uso en esta aplicación |
|---|---|
| `DEBUG` | Confirmar el procesamiento de una línea. |
| `INFO` | Informar inicio y final del reporte. |
| `WARNING` | Señalar una fila rechazada mientras el proceso continúa. |
| `ERROR` | Registrar que el reporte no pudo generarse. |
| `CRITICAL` | Reservado para fallos que impidan continuar una aplicación; aquí no hace falta. |

Ejecuta con `INFO` y luego cambia a `DEBUG`. Observa qué mensajes aparecen.
`logger.info("Reading input file: %s", path)` deja el formato del mensaje a logging.
No se imprime el registro completo cuando falla: el número de línea basta para
localizarlo en esta práctica.

### Destinos y formato

Un **logger** emite eventos. Un **handler** los dirige a un destino. Un
**formatter** controla su presentación. Los niveles filtran los eventos.

Crea `readings/logging_config.py` desde
[logging_config.py](./proyecto/readings/logging_config.py). La configuración de
referencia pone el logger raíz en `DEBUG` y define el umbral de cada handler:
la consola utiliza el nivel solicitado y el archivo opcional recibe desde `DEBUG`.
El logger de `readings.processing` hereda el nivel y propaga sus registros al raíz.

Solo el logger raíz tiene handlers; añadir el mismo destino también a un logger
hijo puede duplicar mensajes por propagación. `basicConfig()` no reconfigura
normalmente un raíz que ya tenga handlers: por eso este código se configura una
vez al iniciar un proceso nuevo. No lo uses como si fuera una celda reiniciable.
[Referencia de logging](https://docs.python.org/3/library/logging.html).

**Extensión opcional:** el archivo usa `RotatingFileHandler` con `maxBytes=100_000`
y `backupCount=2`. Al rotar conserva hasta dos copias numeradas además del archivo
activo. Es una rotación por tamaño, no por fecha; no representa un límite exacto
al byte para cada registro. Para comenzar basta el handler de consola.
[Handlers de archivo](https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler).

## 7. Recibir argumentos y comunicar errores

Reemplaza `main.py` por la [versión completa](./proyecto/main.py). Recorre su flujo:
`argparse` recibe la ruta, se configura logging, se ejecuta `summarize_file` y se
presenta el reporte. `Path` conserva una ruta como objeto. Las rutas relativas
parten de la carpeta donde se ejecuta el comando.

```bash
uv run python main.py --help
uv run python main.py data/readings.jsonl
uv run python main.py data/readings.jsonl --log-level DEBUG
uv run python main.py data/invalid.jsonl
uv run python main.py data/missing.jsonl
```

Dentro de un `except`, `logger.exception()` emite un evento `ERROR` con traceback.
El programa devuelve `1` y no imprime un reporte cuando falla. Los argumentos
incorrectos producen el código `2` de `argparse`. Una fila inválida que se omite
no cambia a error una ejecución que sí produjo el reporte.

Para consultar el código inmediatamente después de ejecutar: `echo $?` en
macOS/Linux o `$LASTEXITCODE` en PowerShell.

```bash
uv run python main.py data/readings.jsonl > report.json
uv run python main.py data/readings.jsonl --log-level ERROR --log-file logs/app.log
```

`StreamHandler` escribe en stderr por defecto. Por ello la primera redirección
guarda el JSON de stdout y los logs siguen visibles. En la segunda ejecución,
la consola queda sin mensajes, pero el archivo conserva detalles y advertencias.
En Windows usa PowerShell 7 o un editor que detecte la codificación al abrir el
JSON redirigido; las versiones antiguas de PowerShell pueden redirigir como UTF-16.

## 8. Compartir un entorno reproducible

Para continuar un proyecto existente, usa su lockfile:

```bash
uv sync --locked
uv run --locked python main.py data/readings.jsonl
```

`--locked` verifica que las declaraciones y el lockfile sean compatibles y falla
si necesita cambiar la resolución. `--frozen` omite esa comprobación de vigencia;
no es un sustituto de `--locked` al revisar una entrega. Un `uv sync` normal puede
actualizar el lockfile. [Bloqueo y sincronización](https://docs.astral.sh/uv/concepts/projects/sync/).

El lockfile fija dependencias, pero no captura los archivos de entrada, la
configuración del sistema ni todos los factores de una ejecución. Comparte los
datos de muestra, los comandos y la versión elegida de Python. `.python-version`
con `3.13` fija la rama; especifica también el parche si el trabajo requiere una
versión exacta del intérprete.

Copia el [.gitignore](./proyecto/.gitignore). Versiona código, pruebas, datos
pequeños de práctica, README, `.python-version`, `pyproject.toml` y `uv.lock`.
`.venv`, cachés y logs se reconstruyen o se generan al ejecutar.

En tu carpeta nueva, con [Git instalado](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git):

```bash
git init
git status --short
git add .
git diff --cached --stat
git commit -m "Add reproducible readings application"
```

Antes del commit verifica que no aparezcan `.venv` ni logs. Si trabajas dentro de
un repositorio ya existente, usa ese repositorio en vez de inicializar uno anidado.
Git guarda revisiones; uv administra el entorno. Son tareas distintas.

## 9. Reproducir desde otra carpeta

Después del commit, crea una copia limpia desde la carpeta que contiene tu
repositorio independiente:

```bash
git clone ./readings-report readings-report-check
cd readings-report-check
uv sync --locked
uv run --locked python main.py data/readings.jsonl
```

El clon solo incluye archivos guardados en Git. La nueva `.venv` se construye
con el lockfile. Si trabajas con el repositorio del curso completo, clona ese
repositorio y entra después en la subcarpeta del proyecto.

## 10. Cuándo cambiar la estructura

Esta aplicación se ejecuta con `uv run python main.py` desde su carpeta. Si se
necesita instalar un comando independiente del directorio de trabajo o distribuir
la lógica, conviene una aplicación empaquetada con `src/`, un backend de construcción
y un punto de entrada en `[project.scripts]`. Se puede explorar en otra carpeta
con `uv init --package example-app`.

`src/` por sí solo no hace que Python encuentre los módulos: el paquete debe
instalarse en el entorno. Esa evolución cambia la instalación y los imports;
no es necesario imponerla a toda aplicación pequeña.

Continúa con los [ejercicios de organización y logging](./PRACTICA.md).
El último tema es [Calidad de código: pytest, Ruff y Makefile](./CALIDAD.md),
que trabaja sobre esta misma aplicación.
