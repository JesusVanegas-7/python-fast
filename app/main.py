from fastapi import FastAPI
# Importamos los módulos de los enrutadores
from app.enrutador.clientes import rutas_clientes
from app.enrutador.facturas import rutas_facturas
from app.enrutador.transacciones import rutas_transacciones

app = FastAPI()

# Incluimos las rutas agrupándolas con tags profesionales
app.include_router(rutas_clientes, tags=["Clientes"])
app.include_router(rutas_facturas, tags=["Facturas"])
app.include_router(rutas_transacciones, tags=["Transacciones"])

@app.get("/")
def inicio():
    return {"mensaje": "Servidor FastAPI modularizado y funcionando correctamente"} 