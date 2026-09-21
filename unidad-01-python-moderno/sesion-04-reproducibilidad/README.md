# Sesión 4: Organización y reproducibilidad de proyectos con uv

Construiremos una aplicación de consola para validar lecturas y generar un
reporte. El trabajo se realiza en archivos Python y en la terminal.

La [presentación](https://drive.google.com/file/d/1L7z6CxmTSq6CT-fPHlxq593WCAa2HRcI/view?usp=drivesdk) explica los conceptos
e intercala demostraciones en la terminal y el editor.

La [guía de la sesión](./GUIA.md) recorre la creación desde una carpeta nueva.
El [proyecto completo](./proyecto/README.md) permite consultar la implementación
y reproducir el resultado.

## Contenido

1. Proyecto, intérprete, entorno y dependencias.
2. Creación con `uv` y configuración en `pyproject.toml`.
3. `main.py`, módulos, paquetes e imports.
4. Argumentos de terminal y códigos de salida.
5. Logging: niveles, loggers, handlers y formato.
6. Reproducción con `uv.lock` y control de versiones.
7. [Ejercicios y reproducción desde una copia limpia](./PRACTICA.md).
8. [Calidad de código: pytest, Ruff y Makefile](./CALIDAD.md).

El último bloque utiliza la misma aplicación y puede continuarse en otra sesión.

## Resultados de aprendizaje

- Crear y ejecutar una aplicación con dependencias declaradas.
- Separar la entrada del programa, las reglas de datos y el procesamiento.
- Registrar eventos y errores sin mezclarlos con el resultado del programa.
- Reconstruir el entorno y comprobar el comportamiento con herramientas de calidad.

Se retoman funciones, excepciones, imports, modelos Pydantic y lectura de archivos
con `with`. Se necesita una terminal, un editor de texto o código y `uv` instalado;
la guía incluye los pasos de preparación.

## Ejecutar la referencia

Desde la raíz del repositorio:

```bash
cd unidad-01-python-moderno/sesion-04-reproducibilidad/proyecto
uv sync --locked
uv run --locked python main.py data/readings.jsonl
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

Resultado: tres lecturas válidas, una rechazada y temperatura media de `22.0`.
La advertencia se muestra en stderr; el reporte JSON, en stdout.
