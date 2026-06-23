from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

lista_clientes = []

# Modelo de datoss
class Cliente(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None


# READ - Listar todos
@app.get("/clientes")
def listar_clientes():
    return {"Clientes": lista_clientes}


# READ - Listar uno
@app.get("/clientes/{id}")
def listar_cliente(id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente

    return {"mensaje": "Cliente no encontrado"}


# CREATE
@app.post("/clientes")
def crear_cliente(datos_cliente: Cliente):
    lista_clientes.append(datos_cliente)
    return {"mensaje": "Se creó el cliente"}


# UPDATE
@app.put("/clientes/{id}")
def editar_cliente(id: int, datos_cliente: Cliente):

    for indice, cliente in enumerate(lista_clientes):
        if cliente.id == id:
            lista_clientes[indice] = datos_cliente
            return {"mensaje": "Cliente actualizado"}

    return {"mensaje": "Cliente no encontrado"}


# DELETE
@app.delete("/clientes/{id}")
def eliminar_cliente(id: int):

    for indice, cliente in enumerate(lista_clientes):
        if cliente.id == id:
            lista_clientes.pop(indice)
            return {"mensaje": "Cliente eliminado"}

    return {"mensaje": "Cliente no encontrado"}

# =========================
# FACTURAS
# =========================

lista_facturas = []

class Factura(BaseModel):
    id: int
    fecha: str
    valor_total: float
    cliente: str


@app.get("/facturas")
def listar_facturas():
    return {"Facturas": lista_facturas}


@app.get("/facturas/{id}")
def listar_factura(id: int):

    for factura in lista_facturas:
        if factura.id == id:
            return factura

    return {"mensaje": "Factura no encontrada"}


@app.post("/facturas")
def crear_factura(datos_factura: Factura):

    lista_facturas.append(datos_factura)
    return {"mensaje": "Factura creada"}


@app.put("/facturas/{id}")
def editar_factura(id: int, datos_factura: Factura):

    for indice, factura in enumerate(lista_facturas):
        if factura.id == id:
            lista_facturas[indice] = datos_factura
            return {"mensaje": "Factura actualizada"}

    return {"mensaje": "Factura no encontrada"}


@app.delete("/facturas/{id}")
def eliminar_factura(id: int):

    for indice, factura in enumerate(lista_facturas):
        if factura.id == id:
            lista_facturas.pop(indice)
            return {"mensaje": "Factura eliminada"}

    return {"mensaje": "Factura no encontrada"}

# =========================
# TRANSACCIONES
# =========================

lista_transacciones = []

class Transaccion(BaseModel):
    id: int
    vr_unitario: float
    cantidad: int
    factura_id: int


@app.get("/transacciones")
def listar_transacciones():
    return {"Transacciones": lista_transacciones}


@app.get("/transacciones/{id}")
def listar_transaccion(id: int):

    for transaccion in lista_transacciones:
        if transaccion.id == id:
            return transaccion

    return {"mensaje": "Transacción no encontrada"}


@app.post("/transacciones")
def crear_transaccion(datos_transaccion: Transaccion):

    lista_transacciones.append(datos_transaccion)
    return {"mensaje": "Transacción creada"}


@app.put("/transacciones/{id}")
def editar_transaccion(id: int, datos_transaccion: Transaccion):

    for indice, transaccion in enumerate(lista_transacciones):
        if transaccion.id == id:
            lista_transacciones[indice] = datos_transaccion
            return {"mensaje": "Transacción actualizada"}

    return {"mensaje": "Transacción no encontrada"}


@app.delete("/transacciones/{id}")
def eliminar_transaccion(id: int):

    for indice, transaccion in enumerate(lista_transacciones):
        if transaccion.id == id:
            lista_transacciones.pop(indice)
            return {"mensaje": "Transacción eliminada"}

    return {"mensaje": "Transacción no encontrada"}