from sqlmodel import SQLModel, Field, Relationship

# Clase base de Transacción
class TransaccionBase(SQLModel):
    # Configuración de campos con valores por defecto [00:12:14, 00:12:35]
    cantidad: int = Field(default=0)
    valor: float = Field(default=0.0)

# Clase que genera la tabla real en la Base de Datos [00:12:51]
class Transaccion(TransaccionBase, table=True):
    # Configuración de la Llave Primaria [00:13:13]
    id: int | None = Field(default=None, primary_key=True)
    
    # Configuración de la Llave Foránea hacia la tabla 'factura' [00:13:37, 00:13:47]
    factura_id: int = Field(foreign_key="factura.id")