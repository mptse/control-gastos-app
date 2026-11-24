## Rol
Actúa como desarrollador backend con experiencia en FastAPI, Jinja2 y pruebas con pytest.

## Objetivo
Construir la mini-aplicación web de **Control de gastos** con estos requisitos:
1. `GET /` muestra el registro de gastos, un formulario para agregar un gasto y, en cada gasto, un botón para eliminarlo (y opcionalmente un resumen del total acumulado).
2. `POST /api/gastos` recibe `{"concepto": "Almuerzo", "monto": 25.50, "categoria": "Comida"}` (ajusta los campos exactos según el contrato de pruebas) y responde con el código `201` y el gasto creado: `{"id": 1, "concepto": "Almuerzo", "monto": 25.50, "categoria": "Comida"}`. Valida que el concepto tenga entre 1 y 100 caracteres y el monto sea mayor que 0; si no, responde con el código `422`.
3. `GET /api/gastos` devuelve la lista de gastos registrados.
4. `DELETE /api/gastos/{id}` elimina el gasto y responde con el código `204`.
5. Si el gasto no existe, eliminar responde con el código `404`.

## Contexto
Lee `AGENTS.md`. El contrato de la API está en `tests/test_aceptacion.py`: las rutas, los nombres de los campos, los tipos de datos y los códigos de estado deben coincidir exactamente con esas pruebas.

## Restricciones
Usa solo las dependencias de `requirements.txt`.
Define las rutas en `app/main.py` y la lógica de negocio en `app/servicios.py`, sin importar FastAPI en `servicios.py`.
Guarda los datos en memoria, sin base de datos ni archivos.
No modifiques `tests/test_aceptacion.py`.
La página usa HTML, CSS y JavaScript sin librerías externas.

## Formato de salida
Antes de escribir código, muestra el plan con las rutas completas de los archivos que vas a crear y espera mi aprobación. Al terminar, resume en una línea qué hace cada archivo.

## Ejemplo
`POST /api/gastos` con `{"concepto": "Café de la mañana", "monto": 4.5, "categoria": "Bebidas"}` responde con el código `201` y devuelve:
`{"id": 1, "concepto": "Café de la mañana", "monto": 4.5, "categoria": "Bebidas"}`

`DELETE /api/gastos/1` responde con el código `204`.

## Criterio de éxito
`python -m pytest -v` pasa todas las pruebas y `ruff check` no reporta errores. Si después de 3 intentos las pruebas no pasan, detente y explica el problema.