import os

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

if not MONGODB_URL:
    raise RuntimeError(
        "No se encontró la variable de entorno MONGODB_URL. "
        "Verifica que el archivo .env exista en la carpeta backend/ "
        "y contenga MONGODB_URL=<tu_cadena_de_conexión_de_Atlas>."
    )

client = MongoClient(MONGODB_URL, server_api=ServerApi("1"))

db = client["techgear"]

productos_collection = db["productos"]
pedidos_collection = db["pedidos"]


def conectar():
    client.admin.command("ping")
    print("Conexión a MongoDB Atlas exitosa.")


def cerrar_conexion():
    client.close()
    print("Conexión cerrada.")