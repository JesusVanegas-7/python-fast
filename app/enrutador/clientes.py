from fastapi import APIRouter, HTTPException
from typing import List
from ..modelos.clientes import Cliente  # Importación relativa con ".."

rutas_clientes = APIRouter()

lista_clientes = []

@rutas_clientes.get("/clientes")
def listar_clientes():
    return {"Clientes": lista_clientes}

@rutas_clientes.get("/clientes/{id}")
def listar_cliente(id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente
    return {"mensaje": "Cliente no encontrado"}

@rutas_clientes.post("/clientes")
def crear_cliente(datos_cliente: Cliente):
    lista_clientes.append(datos_cliente)
    return {"mensaje": "Se creó el cliente"}

@rutas_clientes.put("/clientes/{id}")
def editar_cliente(id: int, datos_cliente: Cliente):
    for indice, cliente in enumerate(lista_clientes):
        if cliente.id == id:
            lista_clientes[indice] = datos_cliente
            return {"mensaje": "Cliente actualizado"}
    return {"mensaje": "Cliente no encontrado"}

@rutas_clientes.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    for indice, cliente in enumerate(lista_clientes):
        if cliente.id == id:
            lista_clientes.pop(indice)
            return {"mensaje": "Cliente eliminado"}
    return {"mensaje": "Cliente no encontrado"}