import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi


# Ruta de la carpeta backend
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar backend/.env
load_dotenv(BASE_DIR / ".env")


MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ambiente502")


if not MONGODB_URL:
    raise RuntimeError(
        "No se encontró MONGODB_URL en el archivo backend/.env"
    )


# Cliente asíncrono de MongoDB
client = AsyncMongoClient(
    MONGODB_URL,
    server_api=ServerApi(
        version="1",
        strict=True,
        deprecation_errors=True
    )
)


# Base de datos
database = client[DATABASE_NAME]


# Colecciones de TechGear
productos_collection = database["productos"]
pedidos_collection = database["pedidos"]