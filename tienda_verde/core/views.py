from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Producto,Pedido,PedidoProducto
# from django.contrib.auth import logout

# Create your views here.


def inicio(request):
    titulo='Tienda Verde | Inicio'
    nombre = request.user.username.split("@")[0]
    data={
        'titulo':titulo,
        'nombre_usuario':nombre
    }
    return render(request,'core/inicio.html',data)

def iniciar_sesion(request):
    titulo='Inicio sesion | Tienda Verde'
    if request.method=="POST":
        usrname= request.POST['username']
        passwrd= request.POST['password']
        usuario= authenticate(request,username=usrname,password=passwrd)
        if usuario is not None:
            login(request,usuario)
            return redirect('Pagina_inicio')
        else:
            print("MATCHHHHHHHHHHHH ERRADO")
            messages.error(request, 'Inicio de sesión incorrecto, intenta de nuevo.')

    data={
        'titulo':titulo
    }
    return render(request,'registration/login.html',data)


def cerrar_sesion(request):
    logout(request)
    return redirect('Pagina_inicio')

def registro(request):
    titulo='Registro | Tienda Verde'
    if request.method == "POST":
        form= regisCliente(request.POST)
        if form.is_valid():
            usuario=form.save()
            login(request,usuario)
            return redirect('Pagina_inicio')
        else:
            print(form.errors) 
    else:
        form= regisCliente() 

    data={
        'titulo':titulo,
        'form':form
    }
    return render(request,'registration/registro.html',data)

def catalogo(request):
    productos = Producto.objects.all()  
    titulo = 'Catálogo de Productos | Tienda Verde'
    data = {
        'titulo': titulo,
        'productos': productos  
    }
    return render(request, 'core/catalogo.html', data)


# MAnejo de carrito 
@login_required
def carrito(request):
    titulo = 'Tu carrito | Tienda Verde'
    carrito = request.session.get("carrito", {})
    p_en_carrito = []
    total = 0
    for producto_id, datos_producto in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        p_en_carrito.append({
            "producto": producto,
            "nombre": datos_producto["nombre"],
            "precio": datos_producto["precio"],
            "total": datos_producto["total"]
        })
        total += datos_producto["total"]

    data = {
        'titulo': titulo,
        'productos_en_carrito': p_en_carrito,
        'total': total,
    }
    return render(request, 'core/carrito.html', data)

@login_required
def agregar_producto(request,producto_id):
    producto= get_object_or_404(Producto, id=producto_id)
    carrito= request.session.get("carrito", {})
    
    if producto_id not in carrito:
        carrito[producto_id]={
            "nombre": producto.nombre,
            "precio": producto.valor,
            "total": producto.valor 
        }
    else:
        messages.info(request,"Este producto ya existe en el carrito")
        return redirect("Carrito_productos")
        
    
    request.session["carrito"]=carrito
    return redirect("Carrito_productos")

@login_required
def quitar_producto(request,producto_id):
    carrito= request.session.get("carrito",{})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session["carrito"]=carrito
    return redirect('Carrito_productos')

@login_required
def conf_pedido(request):
    print(request.method)
    if request.method == 'POST':
        carrito=request.session.get('carrito',{})
        if not carrito:
            messages.info(request,"No hay productos a confirmar")
            return redirect("Carrito_productos")
        pedido=Pedido(cliente=request.user)
        pedido.save()
        for producto_id,item in carrito.items():
            producto=get_object_or_404(Producto,id=producto_id)
            PedidoProducto.objects.create(pedido=pedido,producto=producto)
        request.session["carrito"]={}
        messages.success(request,"Se ha confirmado correctamente su pedido ")
        return redirect('Pagina_inicio')
    else:
        print("Error .metodo GET no permitido")
        return redirect("Carrito_productos")