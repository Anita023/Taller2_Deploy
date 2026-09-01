from django.urls import path

from . import views


urlpatterns = [
    path("", views.listar_productos, name="productos"),
    path("pedido/", views.crear_pedido, name="crear_pedido"),
    path("pedidos/", views.historial_pedidos, name="historial_pedidos"),
    path("pedidos/<str:pedido_id>/", views.detalle_pedido, name="detalle_pedido"),
]
