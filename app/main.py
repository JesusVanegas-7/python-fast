from fastapi import FastAPI
from app.conexion_bd import crear_db_y_tablas
# Aseguramos que las importaciones apunten bien a la carpeta app.enrutador [00:01:57]
from app.enrutador.clientes import rutas_clientes
from app.enrutador.facturas import rutas_facturas
from app.enrutador.transacciones import rutas_transacciones

app = FastAPI()

@app.on_event("startup")
def on_startup():
    crear_db_y_tablas()

# Incluimos los enrutadores con sus tags globales de documentación [00:03:08]
app.include_router(rutas_clientes, tags=["Clientes"])
app.include_router(rutas_facturas, tags=["Facturas"])
app.include_router(rutas_transacciones, tags=["Transacciones"])

@app.get("/")
def inicio():
    return {"mensaje": "Servidor FastAPI con Listas Globales sincronizadas"}
