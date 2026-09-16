# Notas docentes · Unidad 1, sesión 2

## Alineación y alcance

El plan maestro sitúa aquí type hints, lectura del verificador, BaseModel,
restricciones, validadores, serialización, configuración y modelos anidados.
La práctica contribuye a U1 P2 y U1 P3. Mypy concreta la elección de verificador
reservada al docente; no se añade otro producto evaluable. Pydantic v2 es central;
no se incorporan dataclasses, generadores, servicios ni entrenamiento.

La notebook del Zen ya cubre las 19 reglas en el estado revisado del repositorio.
Esta sesión retoma contratos, errores visibles y claridad sin repetir esa lección.

## Guion sugerido para 120 minutos

| Minutos | Actividad |
|---|---|
| 0–10 | Diagnóstico o cierre pendiente: función, instancia y None |
| 10–30 | Anotaciones y ejercicios 1–2; predecir antes de ejecutar mypy |
| 30–55 | BaseModel, conversiones, restricciones; ejercicio 3 |
| 55–80 | Validadores, configuración y anidación; elegir ejercicios 4–6 |
| 80–105 | Leer el módulo y procesar el lote; ejercicio 7 |
| 105–120 | Iniciar ejercicio 8, revisar evidencia y cierre |

La selección de ejercicios 4–6 es trabajo en aula; los restantes continúan como
práctica independiente de U1 P3. Si el diagnóstico requiere más tiempo, conserva
la distinción entre tipado y validación y continúa la práctica fuera del bloque.

## Preguntas y retroalimentación

- Antes del primer ejemplo: ¿una anotación evita que Python multiplique dos enteros?
  Contrastar ejecución y salida de mypy, sin presentar al verificador como infalible.
- ¿Por qué `float | None` exige atender ausencia? Pedir un ejemplo con cero válido.
- ¿Una etiqueta válida garantiza que el modelo acertó? Diferenciar contrato y verdad.
- ¿Aceptar un número en texto conviene para esta fuente? Hacer explícita la conversión.
- ¿Por qué un espacio satisface longitud mínima? Mostrar el orden de normalización.
- ¿Dos errores equivalen a dos filas rechazadas? Revisar posiciones únicas.
- ¿Una configuración inválida puede ignorarse? Acordar que el lote no arranca.

Errores esperables: confundir nulo con omitible; usar `Any` para ocultar problemas;
atrapar `Exception`; olvidar devolver el valor del validador; interpretar un
umbral como criterio de validez; suponer que `validate_assignment` vigila cambios
internos en listas. Pedir siempre un contraejemplo y una comprobación del contrato.

## Soluciones y evidencia

Las ocho soluciones están en Markdown al final. Las celdas de apoyo permiten
continuar sin haber resuelto todos los ejercicios; no cuentan como entrega del
alumno. El módulo es la demostración reutilizable: el alumno lo extiende con la
función tipada del ejercicio 8 y conserva sus comprobaciones y reporte JSON.

Revisar claridad de tipos, restricciones justificadas, errores localizables,
serialización reversible y casos límite. Usar los criterios existentes de U1 P2
(contratos claros y ausencia de Any injustificado) y U1 P3 (restricciones, errores
útiles, serialización); no asignar ponderaciones nuevas.

## Preparación y verificación

Preparar las dependencias fijadas y ejecutar los comandos del README. Reiniciar
el kernel y ejecutar toda la notebook. La celda que escribe el módulo reemplaza
la copia local: trabajar en una carpeta de práctica si hay modificaciones propias.
No se necesita red después de instalar dependencias. Las comprobaciones del
módulo usan `unittest`, de la biblioteca estándar; pytest se enseña en sesión 4.
