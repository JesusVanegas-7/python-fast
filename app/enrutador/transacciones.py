from fastapi import APIRouter, HTTPException
from typing import List
from ..modelos.transacciones import Transaccion

rutas_transacciones = APIRouter()

lista_transacciones = []

@rutas_transacciones.get("/transacciones")
def listar_transacciones():
    return {"Transacciones": lista_transacciones}

@rutas_transacciones.get("/transacciones/{id}")
def listar_transaccion(id: int):
    for transaccion in lista_transacciones:
        if transaccion.id == id:
            return transaccion
    return {"mensaje": "Transacción no encontrada"}

@rutas_transacciones.post("/transacciones")
def crear_transaccion(datos_transaccion: Transaccion):
    lista_transacciones.append(datos_transaccion)
    return {"mensaje": "Transacción creada"}

@rutas_transacciones.put("/transacciones/{id}")
def editar_transaccion(id: int, datos_transaccion: Transaccion):
    for indice, transaccion in enumerate(lista_transacciones):
        if transaccion.id == id:
            lista_transacciones[indice] = datos_transaccion
            return {"mensaje": "Transacción actualizada"}
    return {"mensaje": "Transacción no encontrada"}

@rutas_transacciones.delete("/transacciones/{id}")
def eliminar_transaccion(id: int):
    for indice, transaccion in enumerate(lista_transacciones):
        if transaccion.id == id:
            lista_transacciones.pop(indice)
            return {"mensaje": "Transacción eliminada"}
    return {"mensaje": "Transacción no encontrada"}