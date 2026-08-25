from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import conectar, cerrar_conexion
from app.routers import productos, pedidos


@asynccontextmanager
async def lifespan(app: FastAPI):
    conectar()
    yield
    cerrar_conexion()


app = FastAPI(
    title="TechGear API",
    description="API para el catálogo de productos y la gestión de pedidos de TechGear.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(productos.router)
app.include_router(pedidos.router)


@app.get("/")
def raiz():
    return {"mensaje": "Bienvenido a la API de TechGear"}