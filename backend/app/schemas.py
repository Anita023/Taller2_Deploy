from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class ProductoCrear(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: str = Field(..., min_length=5, max_length=500)
    categoria: str = Field(..., min_length=2, max_length=50)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    imagen_url: Optional[str] = None


class ProductoRespuesta(ProductoCrear):
    id: str

    model_config = ConfigDict(from_attributes=True)


class ProductoActualizar(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, min_length=5, max_length=500)
    categoria: Optional[str] = Field(None, min_length=2, max_length=50)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    imagen_url: Optional[str] = None


class DetallePedido(BaseModel):
    producto_id: str
    cantidad: int = Field(..., gt=0)


class PedidoCrear(BaseModel):
    cliente_nombre: str = Field(..., min_length=2, max_length=100)
    cliente_email: str = Field(..., min_length=5, max_length=150)
    productos: List[DetallePedido] = Field(..., min_length=1)


class PedidoRespuesta(BaseModel):
    id: str
    cliente_nombre: str
    cliente_email: str
    productos: List[DetallePedido]
    total: float
    estado: str
    fecha: datetime
