from django.contrib import admin
from .models import Producto,Pedido,PedidoProducto
# Register your models here.

class PedidoVendedor(admin.ModelAdmin):
    list_display = ('cliente', 'estado')
    list_filter = ('estado',)

admin.site.register(Producto)
admin.site.register(Pedido,PedidoVendedor)
admin.site.register(PedidoProducto)
