import inspect

from fastapi.testclient import TestClient

import app.servicios as servicios_mod
from app.main import app
from app.servicios import servicio_gastos


def setup_function() -> None:
    servicio_gastos.limpiar()


client = TestClient(app)


def test_servicios_no_importa_fastapi() -> None:
    source = inspect.getsource(servicios_mod)
    assert "fastapi" not in source.lower()


def test_validacion_concepto_y_monto() -> None:
    resp_vacio = client.post(
        "/api/gastos",
        json={"concepto": "", "monto": 10.0, "categoria": "General"},
    )
    assert resp_vacio.status_code == 422

    resp_largo = client.post(
        "/api/gastos",
        json={"concepto": "a" * 101, "monto": 10.0, "categoria": "General"},
    )
    assert resp_largo.status_code == 422

    resp_cero = client.post(
        "/api/gastos",
        json={"concepto": "Café", "monto": 0, "categoria": "Bebidas"},
    )
    assert resp_cero.status_code == 422

    resp_negativo = client.post(
        "/api/gastos",
        json={"concepto": "Café", "monto": -5.0, "categoria": "Bebidas"},
    )
    assert resp_negativo.status_code == 422


def test_vista_principal_muestra_gastos_y_total() -> None:
    client.post(
        "/api/gastos",
        json={"concepto": "Café de la mañana", "monto": 4.5, "categoria": "Bebidas"},
    )
    client.post(
        "/api/gastos",
        json={"concepto": "Almuerzo", "monto": 25.5, "categoria": "Comida"},
    )
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Café de la mañana" in resp.text
    assert "Almuerzo" in resp.text
    assert "$30.00" in resp.text
