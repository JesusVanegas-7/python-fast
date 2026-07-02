from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# Clase base de Factura
class FacturaBase(SQLModel):
    # Campo fecha configurado con un valor por defecto (la fecha actual) [00:04:25]
    fecha: datetime = Field(default_factory=datetime.utcnow) 
    
    # Se comentan las relaciones de memoria para evitar fallos por ahora [00:04:07]
    # cliente: "Cliente"
    # transacciones: list["Transaccion"] = []

    # El cálculo del total se deja retornando 0.0 temporalmente mientras se enlaza la BD [00:05:17]
    @property
    def valor_total(self) -> float:
        return 0.0

# Clase que genera la tabla real en la Base de Datos [00:05:35]
class Factura(FacturaBase, table=True):
    # Configuración de la Llave Primaria [00:05:50]
    id: int | None = Field(default=None, primary_key=True)
    
    # Configuración de la Llave Foránea hacia la tabla 'cliente' [00:07:43, 00:08:16]
    cliente_id: int = Field(foreign_key="cliente.id")