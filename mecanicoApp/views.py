from django.shortcuts import render
from .forms import LoginForm

# Create your views here.
def login(request):
    if request.method == "POST":
        pass
    else:
        return render(request, 'login.html', {"form": LoginForm})

def recepcion(request):
    return render(request, 'recepcion.html')