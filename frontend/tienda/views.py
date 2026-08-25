import requests

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render


def listar_productos(request):
    try:
        respuesta = requests.get(
            f"{settings.FASTAPI_URL}/productos/",
            timeout=10
        )

        respuesta.raise_for_status()
        productos = respuesta.json()

    except requests.exceptions.RequestException as error:
        productos = []

        messages.error(
            request,
            f"No fue posible obtener los productos: {error}"
        )

    return render(
        request,
        "tienda/productos.html",
        {
            "productos": productos,
        }
    )


def crear_pedido(request):
    try:
        respuesta_productos = requests.get(
            f"{settings.FASTAPI_URL}/productos/",
            timeout=10
        )

        respuesta_productos.raise_for_status()
        productos = respuesta_productos.json()

    except requests.exceptions.RequestException as error:
        messages.error(
            request,
            f"No fue posible cargar los productos: {error}"
        )

        return render(
            request,
            "tienda/pedido.html",
            {
                "productos": [],
            }
        )

    if request.method == "POST":
        cliente_nombre = request.POST.get(
            "cliente_nombre",
            ""
        ).strip()

        cliente_email = request.POST.get(
            "cliente_email",
            ""
        ).strip()

        producto_id = request.POST.get(
            "producto_id",
            ""
        ).strip()

        cantidad_texto = request.POST.get(
            "cantidad",
            ""
        ).strip()

        if not cliente_nombre:
            messages.error(
                request,
                "El nombre del cliente es obligatorio."
            )

        elif not cliente_email:
            messages.error(
                request,
                "El correo electrónico es obligatorio."
            )

        elif not producto_id:
            messages.error(
                request,
                "Debes seleccionar un producto."
            )

        elif not cantidad_texto.isdigit():
            messages.error(
                request,
                "La cantidad debe ser un número entero."
            )

        elif int(cantidad_texto) <= 0:
            messages.error(
                request,
                "La cantidad debe ser mayor que cero."
            )

        else:
            datos_pedido = {
                "cliente_nombre": cliente_nombre,
                "cliente_email": cliente_email,
                "productos": [
                    {
                        "producto_id": producto_id,
                        "cantidad": int(cantidad_texto),
                    }
                ],
            }

            try:
                respuesta_pedido = requests.post(
                    f"{settings.FASTAPI_URL}/pedidos/",
                    json=datos_pedido,
                    timeout=10
                )

                if respuesta_pedido.status_code == 201:
                    messages.success(
                        request,
                        "Pedido creado correctamente."
                    )

                    return redirect("productos")

                try:
                    detalle = respuesta_pedido.json().get(
                        "detail",
                        "No fue posible crear el pedido."
                    )

                except ValueError:
                    detalle = (
                        "La API devolvió una respuesta no válida."
                    )

                messages.error(request, str(detalle))

            except requests.exceptions.RequestException as error:
                messages.error(
                    request,
                    f"Error al comunicarse con FastAPI: {error}"
                )

    return render(
        request,
        "tienda/pedido.html",
        {
            "productos": productos,
        }
    )