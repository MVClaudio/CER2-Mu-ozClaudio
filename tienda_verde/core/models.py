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
        total = sum(item.producto.valor * item.cantidad for item in self.pedidoproducto_set.all())
        return total
    
    def __str__(self):
        return f'Pedido  de {self.cliente.username} - {self.estado}'
    
class Carrito(models.Model):
    cliente = models.OneToOneField(User,on_delete=models.CASCADE)
    productos= models.ManyToManyField(Producto,through='CarritoProducto')

    def calcular_total(self):
        total = sum(item.producto.valor * item.cantidad for item in self.carritoproducto_set.all())
        return total
    
    def __str__(self):
        return f'Carrito de {self.cliente.username}'
    

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto} en {self.pedido}"

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto} en {self.carrito}"