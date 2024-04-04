from django.shortcuts import render, redirect
from .forms import LoginForm, CrearReparacionForm, CocheNuevo as CocheForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import datetime
from .models import Cliente, Coche, Reparacion, Factura, Linea, MarcaModelo
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator

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

def reparacion_recepcion(request, id):
    if(is_recepcion(request.user) == False):
        return redirect("/login")
    reparacion = Reparacion.objects.get(pk=id)
    return render(request, 'reparacionRecepcion.html', {"reparacion":reparacion})

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
            return render(request, 'recepcion.html', {"form_crear_reparacion": CrearReparacionForm, "message" : ""})
        else:
            return render(request, 'recepcion.html', {"form_crear_reparacion": CrearReparacionForm})
        
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
        modelos = MarcaModelo.objects.all()  # Create a queryset

    paginator = Paginator(modelos, 8)  # Use the queryset for pagination

    # Access the page object based on the request parameter (assuming you have logic to get the page number)
    page_number = request.GET.get('page')  # Example: Assuming you're using a GET parameter for the page
    page_object = paginator.get_page(page_number)

    # Access the results on the requested page
    modelos_after = list(page_object.object_list.values())
    return JsonResponse(modelos_after,safe=False)


""" 
                return render(request, 'recepcion.html', {"form_crear_reparacion": CrearForm, "message" : "Reparacion creada correctamente"}) """