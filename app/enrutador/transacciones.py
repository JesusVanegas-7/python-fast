from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..modelos.transacciones import Transaccion
from ..modelos.facturas import Factura
from ..conexion_bd import engine

rutas_transacciones = APIRouter()

@rutas_transacciones.get("/transacciones")
def listar_transacciones():
    with Session(engine) as session:
        transacciones = session.exec(select(Transaccion)).all()
        return {"Transacciones": transacciones}

@rutas_transacciones.get("/transacciones/{id}")
def listar_transaccion(id: int):
    with Session(engine) as session:
        transaccion = session.get(Transaccion, id)
        if not transaccion:
            return {"mensaje": "Transacción no encontrada"}
        return transaccion

@rutas_transacciones.post("/transacciones")
def crear_transaccion(datos_transaccion: Transaccion):
    with Session(engine) as session:
        # VALIDACIÓN: Verificamos que la factura exista antes de asociarle la transacción
        factura = session.get(Factura, datos_transaccion.factura_id)
        if not factura:
            return {"mensaje": "Factura no encontrada, no se puede crear la transacción"}
        
        session.add(datos_transaccion)
        session.commit()
        session.refresh(datos_transaccion)
        return {"mensaje": "Transacción creada"}

@rutas_transacciones.put("/transacciones/{id}")
def editar_transaccion(id: int, datos_transaccion: Transaccion):
    with Session(engine) as session:
        transaccion_db = session.get(Transaccion, id)
        if not transaccion_db:
            return {"mensaje": "Transacción no encontrada"}
        
        datos_dict = datos_transaccion.model_dump(exclude_unset=True)
        for key, value in datos_dict.items():
            setattr(transaccion_db, key, value)
            
        session.add(transaccion_db)
        session.commit()
        session.refresh(transaccion_db)
        return {"mensaje": "Transacción actualizada"}

@rutas_transacciones.delete("/transacciones/{id}")
def eliminar_transaccion(id: int):
    with Session(engine) as session:
        transaccion = session.get(Transaccion, id)
        if not transaccion:
            return {"mensaje": "Transacción no encontrada"}
        session.delete(transaccion)
        session.commit()
        return {"mensaje": "Transacción eliminada"}
