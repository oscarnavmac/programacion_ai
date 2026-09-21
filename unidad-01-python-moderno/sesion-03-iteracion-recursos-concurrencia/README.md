# Sesión 3: Iteración, recursos y concurrencia

La [presentación de la sesión](https://drive.google.com/file/d/1gMZ1HGejLwIAsZf80W7OjOz9Ktkw5Arz/view?usp=drivesdk)
introduce los conceptos con ejemplos y ejercicios breves.

La [notebook de la sesión](./u1_n4_iteracion_recursos_concurrencia.ipynb) desarrolla el
procesamiento bajo demanda, el manejo de recursos y la concurrencia con `asyncio`.
Incluye dieciséis ejercicios numerados.

## Contenido

- Iterables, iteradores, `iter()`, `next()` y agotamiento.
- Funciones generadoras, `yield`, expresiones generadoras y consumo parcial.
- Composición de transformaciones y errores diferidos.
- `with`, `__enter__`, `__exit__` y `@contextmanager`.
- Cierre de archivos ante errores e interrupciones del recorrido.
- Procesamiento de registros y comparación de memoria con `tracemalloc`.
- Corrutinas, `async`/`await`, event loop y ejecución secuencial frente a concurrente.
- `TaskGroup`, orden de resultados, cancelación y tiempos límite.
- `async with`, `@asynccontextmanager`, `async for` y `aclosing`.
- Solicitudes concurrentes con un límite de actividad y recursos compartidos.

## Ejecución

[![Abrir en Google Colab](https://img.shields.io/badge/Abrir_en-Google_Colab-F9AB00?logo=googlecolab&logoColor=F9AB00&labelColor=333333)](https://colab.research.google.com/drive/1HKRCn91Q5ZGxFq--79Xwow3G692LyyuM)

Abre la notebook con el botón de Google Colab o usa el archivo del repositorio
en Jupyter. Ejecuta las celdas en orden.
Utiliza la biblioteca estándar. Los archivos de práctica se crean en directorios
temporales.

La celda `%%writefile streaming.py` escribe el módulo de apoyo en el directorio de
trabajo. El mismo módulo está disponible en [streaming.py](./streaming.py).
Cada ejercicio se resuelve en su celda y conserva sus comprobaciones.

Para comprobar el módulo desde esta carpeta:

```bash
python check_streaming.py
python check_async_readings.py
python async_readings.py
```

Las comprobaciones cubren consumo bajo demanda, validación, resúmenes y cierre de
archivos tanto con lectura parcial como ante errores.

La parte asíncrona usa `await` directamente en Jupyter/Colab. El módulo
[async_readings.py](./async_readings.py) usa `asyncio.run(main())` como entrada de script.
El ejemplo representa la latencia de las lecturas con `asyncio.sleep` y permite
observar las tareas activas y el cierre del cliente.

Las secciones 1–10 desarrollan iteración y recursos; las secciones 11–16 incorporan
concurrencia. La extensión con `to_thread` puede consultarse después de la práctica.
Consulta las [fuentes oficiales](./FUENTES.md) para ampliar los conceptos.
