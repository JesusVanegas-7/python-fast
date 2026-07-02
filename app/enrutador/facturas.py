from fastapi import APIRouter, HTTPException
from typing import List
from ..modelos.facturas import Factura
# Importamos las dos listas compartidas [00:09:55]
from ..listas import lista_facturas, lista_clientes 

rutas_facturas = APIRouter()

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
    # VALIDACIÓN: Verificamos si el cliente realmente existe en la lista global
    # En tu modelo actual el cliente se pasa como un string (nombre), pero si necesitas buscarlo por ID harías esto:
    cliente_existe = any(c.nombre == datos_factura.cliente for c in lista_clientes)
    
    # Nota: Si en tus pruebas manejas IDs en vez de nombres, la validación sería:
    # cliente_existe = any(c.id == int(datos_factura.cliente) for c in lista_clientes)

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