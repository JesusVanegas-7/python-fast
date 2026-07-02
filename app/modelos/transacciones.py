from sqlmodel import SQLModel, Field

class Transaccion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    vr_unitario: float
    cantidad: int
    factura_id: int
