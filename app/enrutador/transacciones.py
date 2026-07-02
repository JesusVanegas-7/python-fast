from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from ..modelos.facturas import Factura
# Asegúrate de importar tu modelo Transaccion
from ..modelos.transacciones import Transaccion, TransaccionBase 
from ..conexion_bd import engine

rutas_transacciones = APIRouter()

# Función auxiliar para inyectar la sesión [00:01:40]
def obtener_sesion():
    with Session(engine) as session:
        yield session

# 1. Endpoint: Listar todas las transacciones de la BD [00:04:06]
@rutas_transacciones.get("/transacciones")
def listar_transacciones(mi_sesion: Session = Depends(obtener_sesion)):
    # Consulta resumida en una sola línea usando select [00:04:20]
    return mi_sesion.exec(select(Transaccion)).all()

# 2. Endpoint: Crear transacción vinculada a una factura [00:04:47]
@rutas_transacciones.post("/facturas/{factura_id}/transacciones")
def crear_transaccion(
    factura_id: int, 
    datos_transaccion: TransaccionBase, 
    mi_sesion: Session = Depends(obtener_sesion)
):
    # Primero buscamos si la factura existe en la BD [00:04:58]
    factura_encontrada = mi_sesion.get(Factura, factura_id)
    
    # Si la factura no existe, lanzamos error 400 [00:09:46]
    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con el ID {factura_id} no existe"
        )
    
    # Convertimos los datos a diccionario para manipular el factura_id [00:06:23, 00:07:07]
    transaccion_dic = datos_transaccion.model_dump()
    
    # Inyectamos el ID de la factura a la que pertenece esta transacción [00:07:19]
    transaccion_dic["factura_id"] = factura_id
    
    # Validamos el diccionario con el modelo Transaccion [00:07:26]
    transaccion_validada = Transaccion.model_validate(transaccion_dic)
    
    # Guardamos en la base de datos [00:07:58, 00:08:13]
    mi_sesion.add(transaccion_validada)
    mi_sesion.commit()
    mi_sesion.refresh(transaccion_validada)
    
    return transaccion_validada