from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId

from app.database import productos_collection, pedidos_collection
from app.schemas import PedidoCrear, PedidoRespuesta

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

ESTADOS_VALIDOS = {"pendiente", "confirmado", "enviado", "entregado", "cancelado"}


def pedido_helper(pedido) -> dict:
    return {
        "id": str(pedido["_id"]),
        "cliente_nombre": pedido["cliente_nombre"],
        "cliente_email": pedido["cliente_email"],
        "productos": pedido["productos"],
        "total": pedido["total"],
        "estado": pedido["estado"],
        "fecha": pedido["fecha"],
    }


def obtener_object_id(pedido_id: str) -> ObjectId:
    try:
        return ObjectId(pedido_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de pedido no válido.")


@router.post("/", response_model=PedidoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_pedido(pedido: PedidoCrear):
    total = 0.0
    detalle_productos = []

    for item in pedido.productos:
        try:
            oid_producto = ObjectId(item.producto_id)
        except InvalidId:
            raise HTTPException(
                status_code=400,
                detail=f"ID de producto no válido: {item.producto_id}",
            )

        producto = productos_collection.find_one({"_id": oid_producto})

        if not producto:
            raise HTTPException(
                status_code=404,
                detail=f"Producto no encontrado: {item.producto_id}",
            )

        if producto["stock"] < item.cantidad:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Stock insuficiente para '{producto['nombre']}'. "
                    f"Disponible: {producto['stock']}, solicitado: {item.cantidad}."
                ),
            )

        total += producto["precio"] * item.cantidad
        detalle_productos.append(
            {"producto_id": item.producto_id, "cantidad": item.cantidad}
        )

    nuevo_pedido = {
        "cliente_nombre": pedido.cliente_nombre,
        "cliente_email": pedido.cliente_email,
        "productos": detalle_productos,
        "total": total,
        "estado": "pendiente",
        "fecha": datetime.now(timezone.utc),
    }

    resultado = pedidos_collection.insert_one(nuevo_pedido)

    for item in pedido.productos:
        productos_collection.update_one(
            {"_id": ObjectId(item.producto_id)},
            {"$inc": {"stock": -item.cantidad}},
        )

    creado = pedidos_collection.find_one({"_id": resultado.inserted_id})
    return pedido_helper(creado)


@router.get("/", response_model=list[PedidoRespuesta])
def listar_pedidos():
    pedidos = pedidos_collection.find()
    return [pedido_helper(p) for p in pedidos]


@router.get("/{pedido_id}", response_model=PedidoRespuesta)
def obtener_pedido(pedido_id: str):
    oid = obtener_object_id(pedido_id)
    pedido = pedidos_collection.find_one({"_id": oid})

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado.")

    return pedido_helper(pedido)


@router.patch("/{pedido_id}/estado", response_model=PedidoRespuesta)
def actualizar_estado_pedido(pedido_id: str, estado: str):
    oid = obtener_object_id(pedido_id)

    if estado not in ESTADOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Estado no válido. Usa uno de: {', '.join(ESTADOS_VALIDOS)}.",
        )

    resultado = pedidos_collection.update_one({"_id": oid}, {"$set": {"estado": estado}})

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pedido no encontrado.")

    actualizado = pedidos_collection.find_one({"_id": oid})
    return pedido_helper(actualizado)


@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pedido(pedido_id: str):
    oid = obtener_object_id(pedido_id)
    resultado = pedidos_collection.delete_one({"_id": oid})

    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Pedido no encontrado.")