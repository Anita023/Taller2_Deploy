"""
Script para poblar la API de FastAPI con productos tecnológicos reales.

Requisitos:
    pip install requests

Uso:
    1. Asegúrate de que tu backend FastAPI esté corriendo
       (ej: uvicorn app.main:app --reload --port 8001)
    2. Ajusta BASE_URL si tu puerto es distinto.
    3. Ejecuta: python seed_productos.py
"""

import requests

BASE_URL = "http://127.0.0.1:8001"  # Ajusta si tu puerto es diferente

productos = [
    {
        "nombre": "Mouse Gamer RGB Logitech G203",
        "descripcion": "Mouse óptico para gaming con iluminación RGB personalizable y 6 botones programables.",
        "categoria": "Periféricos",
        "precio": 89900,
        "stock": 15,
        "imagen_url": "https://images.unsplash.com/photo-1527814050087-3793815479db",
    },
    {
        "nombre": "Teclado Mecánico Redragon Kumara",
        "descripcion": "Teclado mecánico compacto con switches azules e iluminación LED.",
        "categoria": "Periféricos",
        "precio": 149900,
        "stock": 10,
        "imagen_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3",
    },
    {
        "nombre": "Audífonos Bluetooth Sony WH-CH520",
        "descripcion": "Audífonos inalámbricos con hasta 50 horas de batería y sonido claro.",
        "categoria": "Audio",
        "precio": 199900,
        "stock": 8,
        "imagen_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e",
    },
    {
        "nombre": "Monitor Gamer 24' Samsung 144Hz",
        "descripcion": "Monitor Full HD de 24 pulgadas con panel de 144Hz para gaming fluido.",
        "categoria": "Monitores",
        "precio": 649900,
        "stock": 5,
        "imagen_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf",
    },
    {
        "nombre": "SSD Kingston NV2 500GB",
        "descripcion": "Unidad de estado sólido NVMe M.2 de alta velocidad para mejorar el rendimiento del equipo.",
        "categoria": "Almacenamiento",
        "precio": 179900,
        "stock": 20,
        "imagen_url": "https://images.unsplash.com/photo-1591405351990-4726e331f141",
    },
    {
        "nombre": "Webcam Logitech C920",
        "descripcion": "Webcam Full HD 1080p con enfoque automático, ideal para videollamadas y streaming.",
        "categoria": "Periféricos",
        "precio": 259900,
        "stock": 12,
        "imagen_url": "https://picsum.photos/seed/webcam/400/300",
    },
]

if __name__ == "__main__":
    exitosos = 0
    fallidos = 0

    for producto in productos:
        try:
            respuesta = requests.post(
                f"{BASE_URL}/productos/",
                json=producto,
                timeout=10,
            )
            if respuesta.status_code in (200, 201):
                print(f"✓ Creado: {producto['nombre']}")
                exitosos += 1
            else:
                print(
                    f"✗ Error creando {producto['nombre']}: "
                    f"{respuesta.status_code} - {respuesta.text}"
                )
                fallidos += 1
        except requests.exceptions.RequestException as error:
            print(f"✗ No se pudo conectar con la API: {error}")
            fallidos += 1

    print(f"\nResumen: {exitosos} creados, {fallidos} fallidos.")
    print("Recuerda borrar manualmente los productos de prueba ('string') desde Atlas o Swagger.")
