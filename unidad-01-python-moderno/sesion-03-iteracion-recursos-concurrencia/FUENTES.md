# Fuentes de la sesión

Consultadas el 20 de septiembre de 2026. Los ejemplos usan la biblioteca estándar.

- [Python: programación funcional, iteradores y generadores](https://docs.python.org/3.13/howto/functional.html).
- [Python: definición de decorador](https://docs.python.org/3.13/glossary.html#term-decorator).
- [Python: functools.wraps](https://docs.python.org/3.13/library/functools.html#functools.wraps).
- [Python: contextlib](https://docs.python.org/3.13/library/contextlib.html): contextmanager, closing, asynccontextmanager y aclosing.
- [Python: corrutinas y tareas](https://docs.python.org/3.13/library/asyncio-task.html): await, TaskGroup, gather, cancelación, timeout y to_thread.
- [Python: ejecución de asyncio](https://docs.python.org/3.13/library/asyncio-runner.html): asyncio.run y restricción de un loop activo en el mismo hilo.
- [Python: primitivas de sincronización](https://docs.python.org/3.13/library/asyncio-sync.html): Event y Semaphore.
- [Python: protocolo asíncrono](https://docs.python.org/3.13/reference/datamodel.html#asynchronous-iterators): iteradores y context managers asíncronos.
- [IPython: autoawait](https://ipython.readthedocs.io/en/stable/interactive/autoawait.html): await en notebooks.

Se usa la API de alto nivel de asyncio. No se depende de obtener y cerrar manualmente
un event loop implícito: ese comportamiento ha cambiado entre versiones de Python.
Las mediciones ilustran las esperas del ejemplo y no prometen una aceleración universal.
