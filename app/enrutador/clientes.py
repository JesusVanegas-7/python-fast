from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from ..modelos.clientes import Cliente
from ..conexion_bd import engine

rutas_clientes = APIRouter()

# Función auxiliar para proveer la sesión como dependencia [00:01:20]
def obtener_sesion():
    with Session(engine) as session:
        yield session

@rutas_clientes.get("/clientes")
def listar_clientes(mi_sesion: Session = Depends(obtener_sesion)):
    clientes = mi_sesion.exec(select(Cliente)).all()
    return {"Clientes": clientes}

@rutas_clientes.get("/clientes/{id}")
def listar_cliente(id: int, mi_sesion: Session = Depends(obtener_sesion)):
    # Buscamos el cliente usando el método .get() de la sesión [00:01:44]
    cliente_bd = mi_sesion.get(Cliente, id)
    
    # Si no existe, lanzamos la excepción HTTP 400 usando 'status' como en el video [00:03:17, 00:06:53]
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente con el ID {id} no existe"
        )
    return cliente_bd

@rutas_clientes.post("/clientes")
def crear_cliente(datos_cliente: Cliente, mi_sesion: Session = Depends(obtener_sesion)):
    mi_sesion.add(datos_cliente)
    mi_sesion.commit()
    mi_sesion.refresh(datos_cliente)
    return {"mensaje": "Se creó el cliente"}

@rutas_clientes.patch("/clientes/{id}")
def editar_cliente(id: int, datos_cliente: Cliente, mi_sesion: Session = Depends(obtener_sesion)):
    # 1. Buscar el cliente en la base de datos [00:04:57]
    cliente_bd = mi_sesion.get(Cliente, id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente con el ID {id} no existe"
        )
    
    # 2. Convertir los datos a diccionario omitiendo lo que no se envió [00:08:16]
    datos_dict = datos_cliente.model_dump(exclude_unset=True)
    
    # 3. Actualizar los campos dinámicamente en el objeto de la BD [00:10:02]
    cliente_bd.sqlmodel_update(datos_dict)
    
    # 4. Guardar los cambios permanentes [00:10:41]
    mi_sesion.add(cliente_bd)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_bd)
    return cliente_bd

@rutas_clientes.delete("/clientes/{id}")
def eliminar_cliente(id: int, mi_sesion: Session = Depends(obtener_sesion)):
    # Buscar si el cliente existe antes de borrarlo [00:12:28]
    cliente_bd = mi_sesion.get(Cliente, id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente con el ID {id} no existe"
        )
        
    # Eliminar de la base de datos [00:12:55]
    mi_sesion.delete(cliente_bd)
    mi_sesion.commit()
    
    # Retorna el mensaje de éxito sin response_model para evitar errores de validación [00:14:11]
    return {"mensaje": f"El cliente con el ID {id} se elimino correctamente"}