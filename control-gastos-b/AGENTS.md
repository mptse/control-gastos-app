# AGENTS.md

## Instrucciones del proyecto
- Aplicación web de **Control de gastos** construida con FastAPI y Jinja2.
- Las rutas HTTP se definen en `app/main.py` y la lógica de negocio en `app/servicios.py`.
- `app/servicios.py` no debe importar FastAPI.
- El almacenamiento es en memoria (sin base de datos ni archivos persistentes).
- No modificar `tests/test_aceptacion.py`.
- La plantilla principal vive en `app/templates/index.html` con CSS/JS minimalista sin librerías externas.
- Ejecutar pruebas con `python -m pytest -v` y linting con `ruff check`.
