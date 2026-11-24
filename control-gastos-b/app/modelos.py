from typing import Literal

from pydantic import BaseModel, Field

EstadoFiltro = Literal["pendientes", "pagados"]


class GastoCrear(BaseModel):
    concepto: str = Field(..., min_length=1, max_length=100)
    monto: float = Field(..., gt=0)
    categoria: str = Field(default="General", min_length=1, max_length=50)
    pagado: bool = False


class GastoEstadoActualizar(BaseModel):
    pagado: bool


class GastoRespuesta(BaseModel):
    id: int
    concepto: str
    monto: float
    categoria: str
    pagado: bool
