from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_usuario(request):
    if request.method == "POST":
        usuario = request.POST['usuario']
        password = request.POST['password']
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            login(request, user)
            if(user.groups.filter(name="recepcion").exists()):
                return render(request, 'recepcion.html')
            
    else:
        return render(request, 'login.html', {"form": LoginForm})

def recepcion(request):
    return render(request, 'recepcion.html')