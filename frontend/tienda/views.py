import requests

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render


def listar_productos(request):
    url = f"{settings.FASTAPI_URL}/productos/"

    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        productos = respuesta.json()

    except requests.exceptions.RequestException:
        productos = []

        messages.error(
            request,
            "No fue posible conectarse con la API de productos."
        )

    return render(
        request,
        "tienda/productos.html",
        {
            "productos": productos,
        }
    )