import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

# Inicializar el cliente de MongoDB
client = AsyncIOMotorClient(MONGODB_URL)

# Seleccionar la base de datos (se creará automaticamente si no existe)
database = client.ambiente502

#Seleccionar la colección (se creará automaticamente si no existe)
collection = database.mesas

# Funcion para probar la conexion a la base de datos 

async def test_connection():
    try: 
        # 1. Verificar la conexion al servidor de MongoDB
        await client.admin.command('Ping')
        print("Conexion a MongoDB exitosa.")


        # 2. Crear un documento de prueba 
        doctest = {
            "Nombre": "Ana Maria Deossa",
            "Edad": "17",
            "Color": "Negro",
        
        }

        #3. Guardar el documento en la colección
        print ("Guardando documento de prueba en la colección...")
        result = await collection.insert_one(doctest)
        print(f"Documento guardado con ID: {result.inserted_id}")   

        # 4. Buscar el dato guardado en la colección
        datarequest = await collection.find_one({"_id": result.inserted_id})
        print(f"Documento encontrado: {datarequest}")

    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")

if __name__ == "__main__":
    # Ejecutar la prueba de conexion
    asyncio.run(test_connection())