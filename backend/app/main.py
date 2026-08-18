from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import client
from app.routers import pedidos, productos


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await client.admin.command("ping")
        print("Conexión a MongoDB Atlas exitosa.")
    except Exception as error:
        print(f"Error de conexión con MongoDB: {error}")
        raise

    yield

    await client.close()
    print("Conexión cerrada.")


app = FastAPI(
    title="TechGear API",
    description="API para administrar productos y pedidos",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(productos.router)
app.include_router(pedidos.router)


@app.get("/", tags=["Inicio"])
async def inicio():
    return {
        "mensaje": "TechGear API funcionando",
        "documentacion": "/docs",
    }


@app.get("/health", tags=["Inicio"])
async def health_check():
    return {
        "estado": "activo",
    }