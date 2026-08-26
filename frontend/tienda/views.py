import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render


def listar_productos(request):
    try:
        respuesta = requests.get(
            f"{settings.FASTAPI_URL}/productos/",
            timeout=5
        )
        respuesta.raise_for_status()
        productos = respuesta.json()

    except requests.exceptions.RequestException:
        productos = []
        messages.error(
            request,
            "No se pudo conectar con el catálogo de productos (API fuera de línea)."
        )

    return render(
        request,
        "tienda/productos.html",
        {"productos": productos}
    )


def crear_pedido(request):
    try:
        respuesta_productos = requests.get(
            f"{settings.FASTAPI_URL}/productos/",
            timeout=5
        )
        respuesta_productos.raise_for_status()
        productos = respuesta_productos.json()

    except requests.exceptions.RequestException:
        messages.error(
            request,
            "No se pudo cargar la lista de productos. Verifique que la API esté encendida."
        )
        return render(request, "tienda/pedido.html", {"productos": []})

    if request.method == "POST":
        cliente_nombre = request.POST.get("cliente_nombre", "").strip()
        cliente_email = request.POST.get("cliente_email", "").strip()
        producto_id = request.POST.get("producto_id", "").strip()
        cantidad_texto = request.POST.get("cantidad", "").strip()

        # Validaciones locales del formulario
        if not cliente_nombre or not cliente_email or not producto_id:
            messages.error(request, "Todos los campos son obligatorios.")
        elif not cantidad_texto.isdigit() or int(cantidad_texto) <= 0:
            messages.error(request, "La cantidad debe ser un número entero mayor a 0.")
        else:
            cantidad = int(cantidad_texto)
            # Validación local de stock disponible previa al envío
            prod_seleccionado = next((p for p in productos if p.get("id") == producto_id), None)

            if prod_seleccionado and prod_seleccionado.get("stock", 0) < cantidad:
                messages.error(
                    request,
                    f"Stock insuficiente. Solo quedan {prod_seleccionado.get('stock')} unidades de {prod_seleccionado.get('nombre')}."
                )
            else:
                datos_pedido = {
                    "cliente_nombre": cliente_nombre,
                    "cliente_email": cliente_email,
                    "productos": [
                        {
                            "producto_id": producto_id,
                            "cantidad": cantidad,
                        }
                    ],
                }

                try:
                    respuesta_pedido = requests.post(
                        f"{settings.FASTAPI_URL}/pedidos/",
                        json=datos_pedido,
                        timeout=5
                    )

                    if respuesta_pedido.status_code == 201:
                        messages.success(request, "¡Pedido creado correctamente!")
                        return redirect("productos")

                    # Si FastAPI responde con error 400 (stock, id inválido, etc.)
                    try:
                        detalle = respuesta_pedido.json().get("detail", "Error al procesar el pedido.")
                    except ValueError:
                        detalle = "La API devolvió una respuesta no válida."

                    messages.error(request, f"Error en la solicitud: {detalle}")

                except requests.exceptions.RequestException:
                    messages.error(
                        request,
                        "No se pudo comunicar con el servicio de pedidos (API fuera de línea)."
                    )

    return render(
        request,
        "tienda/pedido.html",
        {"productos": productos}
    )
