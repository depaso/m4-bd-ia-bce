# Reglas del flujo

## Datos
- Los datos crudos viven en datos/. Nunca se modifican; las versiones limpias se guardan como archivos nuevos en salida/.
- Después de cada filtro, el flujo registra cuántas filas quedan.

## Flujo
- Los parámetros van juntos, arriba.
- Toda falla termina con código de salida distinto de 0 y una línea ERROR en el registro.
- Todo aviso sale como borrador hasta que una persona lo apruebe.

## Modelos
- Un modelo se compara siempre con la línea base (responder la clase más frecuente).
- Una respuesta con confianza menor al umbral va a la lista de revisión humana.
