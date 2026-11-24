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


def test_filtrar_gastos_por_estado() -> None:
    resp_pendiente = client.post(
        "/api/gastos",
        json={"concepto": "Factura de luz", "monto": 120.50, "pagado": False},
    )
    assert resp_pendiente.status_code == 201

    resp_pagado = client.post(
        "/api/gastos",
        json={"concepto": "Internet fibra", "monto": 60.00, "pagado": True},
    )
    assert resp_pagado.status_code == 201

    resp_solo_pendientes = client.get("/api/gastos?estado=pendientes")
    assert resp_solo_pendientes.status_code == 200
    pendientes = resp_solo_pendientes.json()
    assert len(pendientes) == 1
    assert pendientes[0]["id"] == 1
    assert pendientes[0]["concepto"] == "Factura de luz"
    assert pendientes[0]["monto"] == 120.50
    assert pendientes[0]["pagado"] is False

    resp_solo_pagados = client.get("/api/gastos?estado=pagados")
    assert resp_solo_pagados.status_code == 200
    pagados = resp_solo_pagados.json()
    assert len(pagados) == 1
    assert pagados[0]["id"] == 2
    assert pagados[0]["concepto"] == "Internet fibra"
    assert pagados[0]["pagado"] is True

    resp_todos = client.get("/api/gastos")
    assert resp_todos.status_code == 200
    assert len(resp_todos.json()) == 2


def test_filtrar_gastos_estado_invalido_retorna_422() -> None:
    resp = client.get("/api/gastos?estado=invalido")
    assert resp.status_code == 422


def test_interfaz_principal_contiene_botones_filtro() -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Todos" in resp.text
    assert "Pendientes" in resp.text
    assert "Pagados" in resp.text
