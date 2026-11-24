from fastapi.testclient import TestClient

from app.main import app
from app.servicios import servicio_gastos


def setup_function() -> None:
    servicio_gastos.limpiar()


client = TestClient(app)


def test_flujo_completo_gastos() -> None:
    resp_inicio = client.get("/")
    assert resp_inicio.status_code == 200
    assert "Control de gastos" in resp_inicio.text

    payload = {"concepto": "Almuerzo", "monto": 25.50, "categoria": "Comida"}
    resp_crear = client.post("/api/gastos", json=payload)
    assert resp_crear.status_code == 201
    datos = resp_crear.json()
    assert datos["id"] == 1
    assert datos["concepto"] == "Almuerzo"
    assert datos["monto"] == 25.50
    assert datos["categoria"] == "Comida"

    resp_lista = client.get("/api/gastos")
    assert resp_lista.status_code == 200
    assert len(resp_lista.json()) == 1

    resp_borrar = client.delete("/api/gastos/1")
    assert resp_borrar.status_code == 204

    resp_borrar_inexistente = client.delete("/api/gastos/999")
    assert resp_borrar_inexistente.status_code == 404
