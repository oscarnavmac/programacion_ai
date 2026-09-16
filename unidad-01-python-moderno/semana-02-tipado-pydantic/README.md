# Sesión 2: Tipado, Pydantic y modelos de datos

Material de la sesión sobre anotaciones de tipo y validación de datos.

- [Presentación: PEP, anotaciones de tipo y Pydantic](./00_pep_tipado_pydantic.pptx).
- [Notebook: tipado y modelos de datos](./01_tipado_pydantic.ipynb).
- [Módulo reutilizable](./lesson_models.py).
- [Comprobaciones de contratos](./check_contracts.py).

## Recorrido

1. Anotaciones, colecciones, valores opcionales y lectura de errores de mypy.
2. BaseModel, conversiones, modo estricto, restricciones y errores.
3. Validadores, configuración, modelos anidados y serialización.
4. Procesamiento de registros con ocho ejercicios y casos límite.

## Ejecutar en Colab o Jupyter

Descarga y abre `01_tipado_pydantic.ipynb` o súbela a Google Colab. Requiere Python
3.12 o posterior; ejecuta las celdas en orden. Ejecuta en orden desde una sesión limpia.
La primera celda instala Pydantic 2.12.5 y mypy 1.19.1. La instalación necesita red;
el resto de la lección funciona en CPU, sin credenciales ni servicios.

La notebook incluye una celda `%%writefile lesson_models.py` para poder trabajar
sin archivos auxiliares en Colab. **Reemplaza ese archivo en el directorio de
trabajo**: guarda con otro nombre tus cambios propios antes de volver a ejecutarla.
El contenido coincide con el módulo incluido en el repositorio.

## Ejecutar el módulo localmente

Desde esta carpeta, con un entorno Python 3.12+ activo (en Windows puede usarse
`py -3.13` en lugar de `python`):

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

API contrastada con documentación oficial de [Pydantic](https://docs.pydantic.dev/latest/concepts/models/)
y [mypy](https://mypy.readthedocs.io/en/stable/getting_started.html).

Los ejemplos de descuentos y usuarios adaptan código de ArjanCodes. Consulta
[la atribución y licencia](./ARJANCODES_LICENSE.txt).
