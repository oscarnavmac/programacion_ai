# Práctica: una aplicación que otra persona pueda ejecutar

Trabaja sobre la aplicación que construiste en la [guía](./GUIA.md).

## Ejercicio 1: imports y punto de entrada

Ejecuta `uv run python -c "import main"`. Explica por qué no genera un reporte
ni configura handlers. Identifica qué ocurriría si la llamada a `main()` quedara
fuera de la condición `if __name__ == "__main__"`.

## Ejercicio 2: rutas y argumentos

Crea una copia de `data/readings.jsonl` con otra lectura válida. Ejecuta el
programa indicando su ruta, sin modificar `main.py`. Comprueba manualmente el
conteo y la media. Ejecuta también una ruta inexistente y observa el código de salida.

## Ejercicio 3: niveles y destinos

Ejecuta la muestra con `DEBUG`, `INFO` y `ERROR`. Anota qué cambia en los mensajes
y qué permanece igual en el reporte.

Con `--log-level ERROR --log-file logs/app.log`, explica por qué una advertencia
puede aparecer en el archivo y no en la consola. Localiza en el código los dos
umbrales que permiten ese comportamiento.

## Ejercicio 4: mejorar el diagnóstico

La advertencia actual identifica la línea rechazada. Añade el nombre del archivo
al mensaje usando argumentos de logging, sin registrar el contenido completo.
La modificación debe estar en el módulo de procesamiento, no en `main.py`.

## Ejercicio 5: reproducibilidad

Comprueba que `uv sync --locked` funciona en una copia limpia. Explica qué
aportan `pyproject.toml`, `uv.lock` y `.python-version`, y por qué no se entrega
`.venv`.

## Evidencia de esta parte

Entrega tu proyecto con un README que indique instalación, ejecución normal,
ejecución con error y ubicación de los logs. Incluye los datos pequeños utilizados
para comprobarlo y deja los archivos generados fuera de Git.

| Criterio | Evidencia |
|---|---|
| Organización | Entrada del programa y procesamiento en archivos diferentes. |
| Ejecución | La ruta de entrada se elige desde la terminal. |
| Diagnóstico | Los niveles filtran eventos y los errores se observan. |
| Salidas | El reporte sigue siendo JSON válido al redirigir stdout. |
| Reproducción | Una copia limpia ejecuta los comandos del README. |

Después se incorporan las comprobaciones del bloque
[Calidad de código: pytest, Ruff y Makefile](./CALIDAD.md).
