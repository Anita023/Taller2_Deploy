from datetime import datetime, timezone
from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from app.database import pedidos_collection
from app.database import productos_collection
from app.schemas import PedidoCrear, PedidoRespuesta

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


def convertir_pedido(documento: dict) -> dict:
    return {
        "id": str(documento["_id"]),
        "cliente_nombre": documento["cliente_nombre"],
        "cliente_email": documento["cliente_email"],
        "productos": documento["productos"],
        "total": documento["total"],
        "estado": documento["estado"],
        "fecha": documento["fecha"],
    }


@router.post(
    "/",
    response_model=PedidoRespuesta,
    status_code=status.HTTP_201_CREATED
)
async def crear_pedido(pedido: PedidoCrear):
    total = 0
    productos_pedido = []

    for detalle in pedido.productos:
        if not ObjectId.is_valid(detalle.producto_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"ID inválido: {detalle.producto_id}"
            )

        producto = await productos_collection.find_one(
            {"_id": ObjectId(detalle.producto_id)}
        )

        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto no encontrado: {detalle.producto_id}"
            )

        if producto["stock"] < detalle.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para {producto['nombre']}"
            )

        total += producto["precio"] * detalle.cantidad

        productos_pedido.append({
            "producto_id": detalle.producto_id,
            "cantidad": detalle.cantidad
        })

    fecha_actual = datetime.now(timezone.utc)

    nuevo_pedido = {
        "cliente_nombre": pedido.cliente_nombre,
        "cliente_email": pedido.cliente_email,
        "productos": productos_pedido,
        "total": round(total, 2),
        "estado": "pendiente",
        "fecha": fecha_actual,
    }

    resultado = await pedidos_collection.insert_one(nuevo_pedido)

    for detalle in pedido.productos:
        await productos_collection.update_one(
            {"_id": ObjectId(detalle.producto_id)},
            {"$inc": {"stock": -detalle.cantidad}}
        )

    pedido_guardado = await pedidos_collection.find_one(
        {"_id": resultado.inserted_id}
    )

    return convertir_pedido(pedido_guardado)


@router.get("/", response_model=List[PedidoRespuesta])
async def listar_pedidos():
    pedidos = []

    cursor = pedidos_collection.find().sort("fecha", -1)

    async for pedido in cursor:
        pedidos.append(convertir_pedido(pedido))

    return pedidos


@router.get("/{pedido_id}", response_model=PedidoRespuesta)
async def obtener_pedido(pedido_id: str):
    if not ObjectId.is_valid(pedido_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID del pedido no es válido"
        )

    pedido = await pedidos_collection.find_one(
        {"_id": ObjectId(pedido_id)}
    )

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )

    return convertir_pedido(pedido)
