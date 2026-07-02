from sqlmodel import SQLModel, Field

class Cliente(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str | None = None
