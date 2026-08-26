from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId

from app.database import productos_collection
from app.schemas import ProductoCrear, ProductoRespuesta, ProductoActualizar

router = APIRouter(prefix="/productos", tags=["Productos"])


def producto_helper(producto) -> dict:
    return {
        "id": str(producto["_id"]),
        "nombre": producto["nombre"],
        "descripcion": producto["descripcion"],
        "categoria": producto["categoria"],
        "precio": producto["precio"],
        "stock": producto["stock"],
        "imagen_url": producto.get("imagen_url"),
    }


def obtener_object_id(producto_id: str) -> ObjectId:
    try:
        return ObjectId(producto_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de producto no válido.")


@router.post("/", response_model=ProductoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCrear):
    nuevo_producto = producto.model_dump()
    resultado = productos_collection.insert_one(nuevo_producto)
    creado = productos_collection.find_one({"_id": resultado.inserted_id})
    return producto_helper(creado)


@router.get("/", response_model=list[ProductoRespuesta])
def listar_productos():
    productos = productos_collection.find()
    return [producto_helper(p) for p in productos]


@router.get("/{producto_id}", response_model=ProductoRespuesta)
def obtener_producto(producto_id: str):
    oid = obtener_object_id(producto_id)
    producto = productos_collection.find_one({"_id": oid})

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")

    return producto_helper(producto)


@router.put("/{producto_id}", response_model=ProductoRespuesta)
def actualizar_producto(producto_id: str, cambios: ProductoActualizar):
    oid = obtener_object_id(producto_id)

    datos = {k: v for k, v in cambios.model_dump().items() if v is not None}

    if not datos:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar.")

    resultado = productos_collection.update_one({"_id": oid}, {"$set": datos})

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")

    actualizado = productos_collection.find_one({"_id": oid})
    return producto_helper(actualizado)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: str):
    oid = obtener_object_id(producto_id)
    resultado = productos_collection.delete_one({"_id": oid})

    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return {
        "mensaje": "Producto eliminado correctamente"
    }
