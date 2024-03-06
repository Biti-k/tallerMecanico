from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_usuario),
    path('recepcion', include("django.contrib.auth.urls")),
    path('recepcion', views.recepcion)
]