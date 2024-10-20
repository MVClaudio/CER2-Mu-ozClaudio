from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Producto
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

@login_required
def carrito(request):
    
    titulo='Tu carrito | Tienda Verde'
    data={
        'titulo':titulo
    }
    return render(request,'core/carrito.html',data)