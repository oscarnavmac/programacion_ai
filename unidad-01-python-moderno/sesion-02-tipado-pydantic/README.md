# Sesión 2: Tipado, Pydantic y modelos de datos

Material de la sesión sobre anotaciones de tipo y validación de datos.

- [Presentación: PEP, anotaciones de tipo y Pydantic](https://drive.google.com/file/d/1_2Bp0DOJYRTTAVd6tD1gruzsVrnT5Bru/view?usp=drivesdk).
- [Notebook: tipado y modelos de datos](./u1_n3_tipado_pydantic.ipynb).
- [Módulo reutilizable](./lesson_models.py).
- [Comprobaciones de contratos](./check_contracts.py).

## Recorrido

1. Anotaciones, colecciones, valores opcionales y lectura de errores de mypy.
2. BaseModel, conversiones, modo estricto, restricciones y errores.
3. Validadores, configuración, modelos anidados y serialización.
4. Procesamiento de registros con ocho ejercicios y casos límite.
5. Una API pequeña que valida peticiones con Pydantic y FastAPI.

## Ejecutar en Colab o Jupyter

[![Abrir en Google Colab](https://img.shields.io/badge/Abrir_en-Google_Colab-F9AB00?logo=googlecolab&logoColor=F9AB00&labelColor=333333)](https://colab.research.google.com/drive/1iVbFAxw1VvEI4aB-9CsQUfdbp8QzPZSR)

Abre la notebook con el botón de Google Colab o descarga el archivo del repositorio
para trabajar en Jupyter. Ejecuta las celdas en orden desde una sesión limpia.
La primera celda instala las dependencias, incluidas FastAPI y httpx2. La
instalación necesita red; las peticiones del ejemplo se ejecutan dentro de la
notebook con `TestClient`, sin iniciar un servidor.

La notebook incluye una celda `%%writefile lesson_models.py` para poder trabajar
sin archivos auxiliares en Colab. **Reemplaza ese archivo en el directorio de
trabajo**: guarda con otro nombre tus cambios propios antes de volver a ejecutarla.
El contenido coincide con el módulo incluido en el repositorio.

## Ejecutar el módulo localmente

Desde esta carpeta, con un entorno de Python activo:

```bash
python -m pip install -r requirements.txt
python -m mypy --strict --no-incremental lesson_models.py
python check_contracts.py
```

Se esperan cero errores de mypy y `All contract checks passed`.
Si no hay internet en clase, prepara este entorno con anticipación. La preparación
formal de proyectos con uv, Ruff y pytest queda para la sesión 4.

## Entrega y fuentes

Entrega tu copia del módulo con la función de conteos del ejercicio 8, sus
comprobaciones y un reporte JSON reconstruible. Los criterios de revisión están
en la notebook.

API contrastada con documentación oficial de [Pydantic](https://docs.pydantic.dev/latest/concepts/models/),
[mypy](https://mypy.readthedocs.io/en/stable/getting_started.html) y
[FastAPI](https://fastapi.tiangolo.com/tutorial/testing/).
