from dataclasses import dataclass


@dataclass
class Gasto:
    id: int
    concepto: str
    monto: float
    categoria: str = "General"
    pagado: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "concepto": self.concepto,
            "monto": self.monto,
            "categoria": self.categoria,
            "pagado": self.pagado,
        }


class ServicioGastos:
    def __init__(self) -> None:
        self._gastos: dict[int, Gasto] = {}
        self._siguiente_id: int = 1

    def limpiar(self) -> None:
        self._gastos.clear()
        self._siguiente_id = 1

    def listar_gastos(self, estado: str | None = None) -> list[dict[str, object]]:
        gastos = list(self._gastos.values())
        if estado == "pendientes":
            gastos = [g for g in gastos if not g.pagado]
        elif estado == "pagados":
            gastos = [g for g in gastos if g.pagado]
        elif estado is not None:
            raise ValueError(f"Estado no válido: {estado}")
        return [gasto.to_dict() for gasto in gastos]

    def crear_gasto(
        self,
        concepto: str,
        monto: float,
        categoria: str = "General",
        pagado: bool = False,
    ) -> dict[str, object]:
        gasto_id = self._siguiente_id
        self._siguiente_id += 1
        gasto = Gasto(
            id=gasto_id,
            concepto=concepto,
            monto=monto,
            categoria=categoria,
            pagado=pagado,
        )
        self._gastos[gasto_id] = gasto
        return gasto.to_dict()

    def actualizar_estado_pago(self, gasto_id: int, pagado: bool) -> dict[str, object] | None:
        gasto = self._gastos.get(gasto_id)
        if gasto is None:
            return None
        gasto.pagado = pagado
        return gasto.to_dict()

    def eliminar_gasto(self, gasto_id: int) -> bool:
        if gasto_id not in self._gastos:
            return False
        del self._gastos[gasto_id]
        return True

    def total_acumulado(self, estado: str | None = None) -> float:
        gastos = self.listar_gastos(estado=estado)
        return round(sum(float(gasto["monto"]) for gasto in gastos), 2)


servicio_gastos = ServicioGastos()
