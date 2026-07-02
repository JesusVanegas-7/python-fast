from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..modelos.facturas import Factura
from ..modelos.clientes import Cliente
from ..conexion_bd import engine

rutas_facturas = APIRouter()

@rutas_facturas.get("/facturas")
def listar_facturas():
    with Session(engine) as session:
        facturas = session.exec(select(Factura)).all()
        return {"Facturas": facturas}

@rutas_facturas.get("/facturas/{id}")
def listar_factura(id: int):
    with Session(engine) as session:
        factura = session.get(Factura, id)
        if not factura:
            return {"mensaje": "Factura no encontrada"}
        return factura

@rutas_facturas.post("/facturas")
def crear_factura(datos_factura: Factura):
    with Session(engine) as session:
        # VALIDACIÓN: Verificamos si el cliente existe por nombre (según lógica previa)
        # O por ID si se prefiere. Aquí seguimos lo que parece ser la intención original:
        sentencia = select(Cliente).where(Cliente.nombre == datos_factura.cliente)
        cliente_existe = session.exec(sentencia).first()
        
        if not cliente_existe:
            return {"mensaje": "Cliente no encontrado, no se puede crear la factura"}

        session.add(datos_factura)
        session.commit()
        session.refresh(datos_factura)
        return {"mensaje": "Factura creada"}

@rutas_facturas.put("/facturas/{id}")
def editar_factura(id: int, datos_factura: Factura):
    with Session(engine) as session:
        factura_db = session.get(Factura, id)
        if not factura_db:
            return {"mensaje": "Factura no encontrada"}
        
        datos_dict = datos_factura.model_dump(exclude_unset=True)
        for key, value in datos_dict.items():
            setattr(factura_db, key, value)
            
        session.add(factura_db)
        session.commit()
        session.refresh(factura_db)
        return {"mensaje": "Factura actualizada"}

@rutas_facturas.delete("/facturas/{id}")
def eliminar_factura(id: int):
    with Session(engine) as session:
        factura = session.get(Factura, id)
        if not factura:
            return {"mensaje": "Factura no encontrada"}
        session.delete(factura)
        session.commit()
        return {"mensaje": "Factura eliminada"}
