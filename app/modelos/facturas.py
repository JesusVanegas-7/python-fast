from sqlmodel import SQLModel, Field

class Factura(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    fecha: str
    valor_total: float
    cliente: str
