from django.db import models
from django.contrib.auth.models import User

# Create your models here.

estado_choices= [
    ('pendiente','Pendiente'),
    ('completado','Completado'),
]
class Producto(models.Model):
    nombre = models.CharField(max_length=20)
    valor = models.IntegerField()
    stock = models.PositiveIntegerField()
    imagen= models.ImageField(upload_to='imagenes/',null=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    cliente = models.ForeignKey(User,on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto,through='PedidoProducto')
    estado = models.CharField(max_length=20,choices=estado_choices,default='pendiente')
    
    def calcular_total(self):
        total = sum(item.producto.valor for item in PedidoProducto.objects.filter(pedido=self))
        return total
    
    def __str__(self):
        return f'Pedido  de {self.cliente.username} - {self.estado}'
    
class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.producto} en {self.pedido}"