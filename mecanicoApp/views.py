from django.shortcuts import render, redirect
from .forms import LoginForm, CrearReparacionForm, CocheNuevo as CocheForm, AgregarLinea
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import datetime
import os
from .models import Cliente, Coche, Reparacion, Factura, Linea, MarcaModelo, Pack, TipoLinea
from django.http import JsonResponse
import json
from django.conf import settings 
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from django.contrib.auth import logout



def is_recepcion(user):
    if (user.groups.filter(name="recepcion").exists()):
        return True
    else:
        return False
            
def is_mecanico(user):
    if (user.groups.filter(name="mecanico").exists()):
        return True
    else:
        return False

# Create your views here.
def index(request):
    if(request.user.is_authenticated):
        if(request.user.groups.filter(name="recepcion").exists()):
            return redirect("/recepcion")
        elif(request.user.groups.filter(name="mecanico").exists()):
            return redirect("/mecanico")
        else:
            return redirect("/login")
    else:
        return redirect("/login")

def mecanico(request):
    if(is_mecanico(request.user) == False):
        return redirect("/login")
    reparaciones = Reparacion.objects.filter(estado="A")
    return render(request, 'mecanico.html', {"reparaciones":reparaciones})

def reparacion(request, id):
    if(is_mecanico(request.user) == False):
        return redirect("/login")
    reparacion = Reparacion.objects.get(pk=id, estado="A")
    lineas = Linea.objects.filter(reparacion=id)
    return render(request, 'reparacion.html', {"reparacion":reparacion, "lineas":lineas})

def agregar_linea(request, id_reparacion):
    if(is_mecanico(request.user) == True or is_recepcion(request.user) == True):
        reparacion = Reparacion.objects.get(pk=id_reparacion)
        packs = Pack.objects.all()
        if(request.method == "GET"):
            return render(request, 'agregar_linea.html', {"reparacion":reparacion, "form": AgregarLinea, "packs":packs})
        elif(request.method == "POST"):
            if(request.POST["tipo_linea"] == "M"):
                tipo_linea = TipoLinea.objects.get(pk=request.POST["tipo_linea"])
                linea = Linea(tarea=request.POST["descripcion"], reparacion=reparacion,cantidad=request.POST["cantidad"], precio=0,precio_total=0,tipo=tipo_linea, descuento=request.POST["descuento"])
                linea.save()
            elif(request.POST["tipo_linea"] == "O"):
                precio_total = float(request.POST["precio"]) - float(request.POST["precio"]) * float(request.POST["descuento"]) / 100
                tipo_linea = TipoLinea.objects.get(pk=request.POST["tipo_linea"])
                linea = Linea(tarea=request.POST["descripcion"], reparacion=reparacion,cantidad=request.POST["cantidad"], precio=request.POST["precio"],precio_total=precio_total,tipo=tipo_linea, descuento=request.POST["descuento"])
                linea.save()
            elif(request.POST["tipo_linea"] == "R"):
                precio_total = float(request.POST["precio"]) * float(request.POST['cantidad'])
                precio_total = precio_total - float(request.POST["descuento"]) / 100
                tipo_linea = TipoLinea.objects.get(pk=request.POST["tipo_linea"])
                linea = Linea(tarea=request.POST["descripcion"], reparacion=reparacion,cantidad=request.POST["cantidad"], precio=request.POST["precio"],precio_total=precio_total,tipo=tipo_linea, descuento=request.POST["descuento"])
                linea.save()
            elif(request.POST["tipo_linea"] == "P"):
                if(request.POST["pack"] == ""):
                    return render(request, 'agregar_linea.html', {"reparacion":reparacion, "form": AgregarLinea, "packs":packs, "error":"Selecciona un pack!"})
                pack = Pack.objects.get(pk=request.POST["pack"])
                precio_total = float(pack.coste) - float(request.POST["descuento"]) / 100
                tipo_linea = TipoLinea.objects.get(pk=request.POST["tipo_linea"])
                linea = Linea(tarea=pack.accion, reparacion=reparacion,cantidad=request.POST["cantidad"], precio=pack.coste,precio_total=precio_total,tipo=tipo_linea, descuento=request.POST["descuento"])
                linea.save()
            if(is_mecanico(request.user)):
                return redirect("reparacion", id=id_reparacion)
            elif(is_recepcion(request.user)):
                return redirect("reparacion_recepcion", id=id_reparacion)


def eliminar_linea(request, id_linea):
    if(is_mecanico(request.user) or is_recepcion(request.user)):
        linea = Linea.objects.get(pk=id_linea)
        linea.delete()
        if(is_mecanico(request.user)):
            return redirect("reparacion", id=linea.reparacion.id)
        elif(is_recepcion(request.user)):
            return redirect("reparacion_recepcion", id=linea.reparacion.id)
    return redirect("/")

def rechazar_reparacion(request, id_reparacion):
    reparacion = Reparacion.objects.get(pk=id_reparacion)
    reparacion.estado = "R"
    reparacion.save()
    return redirect("mecanico")

def reparacion_recepcion(request, id):
    if(is_recepcion(request.user) == False):
        return redirect("/login")
    reparacion = Reparacion.objects.get(pk=id)
    lineas = Linea.objects.filter(reparacion=reparacion)
    return render(request, 'reparacionRecepcion.html', {"reparacion":reparacion, "lineas":lineas})

def login_usuario(request):        
    if request.method == "POST":
        usuario = request.POST['usuario']
        password = request.POST['password']
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            login(request, user)
            if(user.groups.filter(name="recepcion").exists()):
                return redirect("recepcion")
            if(is_mecanico(user)):
                return redirect("mecanico")
        else:
            return render(request, 'login.html', {"form": LoginForm, "error_message": "Usuario o password incorrecto"})
    else:
        return render(request, 'login.html', {"form": LoginForm})

def coche_nuevo(request, cliente):
    if(not request.user.is_authenticated):
        return redirect("/login");
    if(request.method == "POST"):
        form = CocheForm(request.POST)
        if form.is_valid():
            coche = Coche(cliente=Cliente.objects.get(pk=cliente), matricula=request.POST['matricula'], modelo=MarcaModelo.objects.get(pk=request.POST['modelo']), km=request.POST['km'])
            coche.save()
            return redirect("recepcion")
    return render(request, 'coche_nuevo.html', {"cliente": cliente, "form":CocheForm})

def recepcion(request):
    if(is_mecanico(request.user)):
        return redirect("/login")
    elif(is_recepcion(request.user)):
        reparaciones = Reparacion.objects.filter(estado="C")
        if request.method == "POST":
            accion = request.POST['action']
            if(accion == "crear_reparacion"):
                cliente = Cliente.objects.get(pk=request.POST['cliente'])
                coche_id = request.POST['coche']
                if(coche_id == "-1"):
                    return render(request, 'recepcion.html', {"form_crear_reparacion": CrearReparacionForm, "message" : "Selecciona un coche valido"})
                coche = Coche.objects.get(pk=request.POST['coche'])
                fecha = datetime.datetime.now()
                reparacion = Reparacion(cliente=cliente, coche=coche, fecha=fecha, estado="A")
                reparacion.save()
                return redirect("reparacion_recepcion", reparacion.pk)
            elif(accion == "coche_nuevo"):
                cliente = request.POST["cliente"]
                return redirect("coche_nuevo", cliente)
            return render(request, 'recepcion.html', {"form_crear_reparacion": CrearReparacionForm, "message" : "", "reparaciones" : reparaciones })
        else:
            todo = False
            if(request.GET.get("todo")):
                reparaciones = Reparacion.objects.all()
                todo = True
            return render(request, 'recepcion.html', {"form_crear_reparacion": CrearReparacionForm, "reparaciones" : reparaciones, "todo" : todo})
    else:
        return redirect("/login")
        
def get_coches_cliente(request):
    cliente = Cliente.objects.get(pk=request.GET['cliente_id'])
    coches = list(Coche.objects.filter(cliente=cliente).values())
    for coche in coches:
        coche['modelo'] = MarcaModelo.objects.get(pk=coche['modelo_id']).modelo
        
    return JsonResponse(coches,safe=False)

def get_modelos(request):
    if(request.GET.get('filtro')):
        modelos = MarcaModelo.objects.filter(modelo__icontains=request.GET.get('filtro'))
    else:
        modelos = MarcaModelo.objects.all()

    paginator = Paginator(modelos, 8)

    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    modelos_after = list(page_object.object_list.values())
    return JsonResponse(modelos_after,safe=False)

def modificar_linea_recepcion(request, id):
    linea = Linea.objects.get(pk=id)
    if(is_recepcion(request.user)):
        if(request.method == 'GET'):
            return render(request, 'modificar_linea_recepcion.html', {"linea" : linea})
        elif(request.method == 'POST'):
            desc = request.POST.get('descuento')
            linea.descuento = desc
            if(not linea.precio):
                linea.precio = 0
            precio_total = float(linea.cantidad) * float(linea.precio)
            linea.precio_total = precio_total - float(precio_total) * float(linea.descuento) / 100
            linea.save()
            
            return redirect("reparacion_recepcion", id=linea.reparacion.id)
    else:
        return redirect("/login")
    
def modificar_linea_mecanico(request, id):
    linea = Linea.objects.get(pk=id)
    packs = Pack.objects.all()
    if(is_mecanico(request.user)):
        if(request.method == "GET"):
            return render(request, 'modificar_linea_mecanico.html', {"linea" : linea, "packs" : packs})
        elif(request.method == 'POST'):
            if(linea.tipo.tipo == "M"):
                descripcion = request.POST.get("descripcion")
                cantidad = request.POST.get("cantidad")
                linea.tarea = descripcion
                linea.cantidad = cantidad
                linea.save()
            elif(linea.tipo.tipo == "P"):
                pack = request.POST.get("pack")
                packInstance = Pack.objects.get(pk=pack)
                linea.pack = packInstance
                linea.tarea = packInstance.accion
                linea.precio = packInstance.coste
                linea.precio_total = linea.precio - linea.precio * linea.descuento / 100
                linea.save()
            elif(linea.tipo.tipo == "R"):
                linea.tarea = request.POST["descripcion"]
                linea.cantidad = request.POST["cantidad"]
                linea.precio = request.POST["precio"]
                linea.precio_total = float(linea.precio) * float(linea.cantidad)
                linea.precio_total = linea.precio_total - linea.precio_total * float(linea.descuento) / 100
                linea.save()
            elif(linea.tipo.tipo == "O"):
                linea.tarea = request.POST["descripcion"]
                linea.cantidad = request.POST["cantidad"]
                linea.precio = request.POST["precio"]
                linea.precio_total = float(linea.precio) * float(linea.cantidad)
                linea.precio_total = linea.precio_total - linea.precio_total * float(linea.descuento) / 100
                linea.save()
            return redirect("reparacion", id=linea.reparacion.id)
    else:
        return redirect("/login")
    
def logout_view(request):
    logout(request)
    return redirect("/login")

def cerrar_reparacion(request, id_reparacion):
    reparacion = Reparacion.objects.get(pk=id_reparacion)
    reparacion.estado = "C"
    reparacion.save()
    return redirect("mecanico")


def facturas(request):
    if(is_recepcion(request.user)):
        reparaciones = Reparacion.objects.filter(estado="F")
        return render(request, "facturas.html", {"reparaciones":reparaciones})
    else:
        return redirect("/login")

def facturar_reparacion(request, id):
    if(is_recepcion(request.user)):
        reparacion = Reparacion.objects.get(pk=id)
        reparacion.estado = 'F'
        reparacion.save()
        return redirect("facturas")
    else:
        return redirect("/login")