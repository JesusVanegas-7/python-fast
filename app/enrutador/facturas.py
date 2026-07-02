from fastapi import APIRouter, HTTPException
from typing import List
from ..modelos.facturas import Factura

rutas_facturas = APIRouter()

lista_facturas = []

@rutas_facturas.get("/facturas")
def listar_facturas():
    return {"Facturas": lista_facturas}

@rutas_facturas.get("/facturas/{id}")
def listar_factura(id: int):
    for factura in lista_facturas:
        if factura.id == id:
            return factura
    return {"mensaje": "Factura no encontrada"}

@rutas_facturas.post("/facturas")
def crear_factura(datos_factura: Factura):
    lista_facturas.append(datos_factura)
    return {"mensaje": "Factura creada"}

@rutas_facturas.put("/facturas/{id}")
def editar_factura(id: int, datos_factura: Factura):
    for indice, factura in enumerate(lista_facturas):
        if factura.id == id:
            lista_facturas[indice] = datos_factura
            return {"mensaje": "Factura actualizada"}
    return {"mensaje": "Factura no encontrada"}

@rutas_facturas.delete("/facturas/{id}")
def eliminar_factura(id: int):
    for indice, factura in enumerate(lista_facturas):
        if factura.id == id:
            lista_facturas.pop(indice)
            return {"mensaje": "Factura eliminada"}
    return {"mensaje": "Factura no encontrada"}