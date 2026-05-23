from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

lista_clientes = []

# Modelo de datos
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