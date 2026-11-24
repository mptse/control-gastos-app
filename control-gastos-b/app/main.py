import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

APP_DIR = Path(__file__).resolve().parent

try:
    from app.modelos import (
        EstadoFiltro,
        GastoCrear,
        GastoEstadoActualizar,
        GastoRespuesta,
    )
    from app.servicios import servicio_gastos
except ModuleNotFoundError:
    sys.path.insert(0, str(APP_DIR.parent))
    from app.modelos import (
        EstadoFiltro,
        GastoCrear,
        GastoEstadoActualizar,
        GastoRespuesta,
    )
    from app.servicios import servicio_gastos

app = FastAPI(title="Control de gastos")
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request) -> HTMLResponse:
    gastos = servicio_gastos.listar_gastos()
    total = servicio_gastos.total_acumulado()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "gastos": gastos,
            "total": total,
        },
    )


@app.post("/api/gastos", response_model=GastoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_gasto(payload: GastoCrear) -> dict:
    return servicio_gastos.crear_gasto(
        concepto=payload.concepto,
        monto=payload.monto,
        categoria=payload.categoria,
        pagado=payload.pagado,
    )


@app.get("/api/gastos", response_model=list[GastoRespuesta])
def listar_gastos(estado: EstadoFiltro | None = None) -> list:
    return servicio_gastos.listar_gastos(estado=estado)


@app.patch("/api/gastos/{gasto_id}", response_model=GastoRespuesta)
def actualizar_estado_gasto(gasto_id: int, payload: GastoEstadoActualizar) -> dict:
    actualizado = servicio_gastos.actualizar_estado_pago(gasto_id=gasto_id, pagado=payload.pagado)
    if actualizado is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gasto no encontrado")
    return actualizado


@app.delete("/api/gastos/{gasto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_gasto(gasto_id: int) -> Response:
    eliminado = servicio_gastos.eliminar_gasto(gasto_id)
    if not eliminado:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
