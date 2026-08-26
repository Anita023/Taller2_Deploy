from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from app.database import productos_collection
from app.schemas import (
    ProductoActualizar,
    ProductoCrear,
    ProductoRespuesta,
)

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


def convertir_producto(documento: dict) -> dict:
    return {
        "id": str(documento["_id"]),
        "nombre": documento["nombre"],
        "descripcion": documento["descripcion"],
        "categoria": documento["categoria"],
        "precio": documento["precio"],
        "stock": documento["stock"],
        "imagen_url": documento.get("imagen_url"),
    }


@router.get("/", response_model=List[ProductoRespuesta])
async def listar_productos():
    productos = []

    cursor = productos_collection.find()

    async for producto in cursor:
        productos.append(convertir_producto(producto))

    return productos


@router.get("/{producto_id}", response_model=ProductoRespuesta)
async def obtener_producto(producto_id: str):
    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID del producto no es válido"
        )

    producto = await productos_collection.find_one(
        {"_id": ObjectId(producto_id)}
    )

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return convertir_producto(producto)


@router.post(
    "/",
    response_model=ProductoRespuesta,
    status_code=status.HTTP_201_CREATED
)
async def crear_producto(producto: ProductoCrear):
    nuevo_producto = producto.model_dump()

    resultado = await productos_collection.insert_one(nuevo_producto)

    producto_guardado = await productos_collection.find_one(
        {"_id": resultado.inserted_id}
    )

    return convertir_producto(producto_guardado)


@router.put("/{producto_id}", response_model=ProductoRespuesta)
async def actualizar_producto(
    producto_id: str,
    producto: ProductoActualizar
):
    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID del producto no es válido"
        )

    datos = producto.model_dump(exclude_unset=True)

    if not datos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se enviaron datos para actualizar"
        )

    resultado = await productos_collection.update_one(
        {"_id": ObjectId(producto_id)},
        {"$set": datos}
    )

    if resultado.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    producto_actualizado = await productos_collection.find_one(
        {"_id": ObjectId(producto_id)}
    )

    return convertir_producto(producto_actualizado)


@router.delete("/{producto_id}")
async def eliminar_producto(producto_id: str):
    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID del producto no es válido"
        )

    resultado = await productos_collection.delete_one(
        {"_id": ObjectId(producto_id)}
    )

    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return {
        "mensaje": "Producto eliminado correctamente"
    }
