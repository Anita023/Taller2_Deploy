import asyncio
from datetime import datetime, timezone

from app.database import (
    client,
    database,
    productos_collection,
)


async def test_connection():
    try:
        # 1. Verificar conexión
        await client.admin.command("ping")
        print("Conexión a MongoDB Atlas exitosa.")

        # 2. Crear un producto de prueba
        producto_prueba = {
            "nombre": "Producto de prueba",
            "descripcion": "Documento creado para comprobar la conexión",
            "categoria": "Pruebas",
            "precio": 1000.0,
            "stock": 1,
            "imagen_url": None,
            "fecha_creacion": datetime.now(timezone.utc),
        }

        # 3. Guardar documento
        resultado = await productos_collection.insert_one(
            producto_prueba
        )

        print(
            f"Producto guardado con ID: {resultado.inserted_id}"
        )

        # 4. Buscar documento
        documento = await productos_collection.find_one(
            {"_id": resultado.inserted_id}
        )

        print(f"Documento encontrado: {documento}")

    except Exception as error:
        print(f"Error al conectar con MongoDB: {error}")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(test_connection())