from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..modelos.clientes import Cliente
from ..conexion_bd import engine

rutas_clientes = APIRouter()

@rutas_clientes.get("/clientes")
def listar_clientes():
    with Session(engine) as session:
        clientes = session.exec(select(Cliente)).all()
        return {"Clientes": clientes}

@rutas_clientes.get("/clientes/{id}")
def listar_cliente(id: int):
    with Session(engine) as session:
        cliente = session.get(Cliente, id)
        if not cliente:
            return {"mensaje": "Cliente no encontrado"}
        return cliente

@rutas_clientes.post("/clientes")
def crear_cliente(datos_cliente: Cliente):
    with Session(engine) as session:
        session.add(datos_cliente)
        session.commit()
        session.refresh(datos_cliente)
        return {"mensaje": "Se creó el cliente"}

@rutas_clientes.put("/clientes/{id}")
def editar_cliente(id: int, datos_cliente: Cliente):
    with Session(engine) as session:
        cliente_db = session.get(Cliente, id)
        if not cliente_db:
            return {"mensaje": "Cliente no encontrado"}
        
        datos_dict = datos_cliente.model_dump(exclude_unset=True)
        for key, value in datos_dict.items():
            setattr(cliente_db, key, value)
        
        session.add(cliente_db)
        session.commit()
        session.refresh(cliente_db)
        return {"mensaje": "Cliente actualizado"}

@rutas_clientes.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    with Session(engine) as session:
        cliente = session.get(Cliente, id)
        if not cliente:
            return {"mensaje": "Cliente no encontrado"}
        session.delete(cliente)
        session.commit()
        return {"mensaje": "Cliente eliminado"}
