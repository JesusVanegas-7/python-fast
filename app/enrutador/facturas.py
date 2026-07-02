from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from ..modelos.clientes import Cliente
# Asegúrate de importar tus modelos de facturas desde tus archivos locales
from ..modelos.facturas import Factura, FacturaBase 
from ..conexion_bd import engine

rutas_facturas = APIRouter()

# Función auxiliar para inyectar la sesión en los endpoints [00:01:20]
def obtener_sesion():
    with Session(engine) as session:
        yield session

# 1. Endpoint: Listar todas las facturas de la base de datos [00:01:02]
@rutas_facturas.get("/facturas")
def listar_facturas(mi_sesion: Session = Depends(obtener_sesion)):
    # Ejecuta el select mapeando la entidad Factura [00:03:15, 00:04:03]
    facturas = mi_sesion.exec(select(Factura)).all()
    return {"Facturas": facturas}

# 2. Endpoint: Crear una factura vinculada a un cliente por ID [00:06:26]
@rutas_facturas.post("/clientes/{cliente_id}/facturas")
def crear_factura(
    cliente_id: int, 
    datos_factura: FacturaBase, 
    mi_sesion: Session = Depends(obtener_sesion)
):
    # Buscar el cliente en la base de datos con el método .get() [00:07:43]
    cliente_bd = mi_sesion.get(Cliente, cliente_id)
    
    # Validación: Si el cliente no existe en la BD, lanza error 400 [00:09:06]
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente con el ID {cliente_id} no existe"
        )
    
    # Convertir el JSON de entrada a un diccionario de Python [00:10:37]
    # ¡Ojo con los paréntesis en .model_dump()! Al profe se le olvidaron al inicio y le dio error [00:16:48]
    factura_dic = datos_factura.model_dump()
    
    # Inyectar manualmente el cliente_id de la URL dentro del diccionario [00:11:50]
    factura_dic["cliente_id"] = cliente_id
    
    # Validar y construir la instancia final del modelo Factura listo para la BD [00:12:15]
    factura_validada = Factura.model_validate(factura_dic)
    
    # Guardar permanentemente en la base de datos de SQLite [00:13:03, 00:13:34]
    mi_sesion.add(factura_validada)
    mi_sesion.commit()
    mi_sesion.refresh(factura_validada)
    
    return factura_validada