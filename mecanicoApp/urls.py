from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_usuario, name="login"),
    path('recepcion/', include("django.contrib.auth.urls")),
    path('recepcion/', views.recepcion, name="recepcion"),
    path('mecanico/', views.mecanico, name="mecanico"),
    path('recepcion/coche_nuevo/<str:cliente>', views.coche_nuevo, name="coche_nuevo"),
    path('get_coches_cliente', views.get_coches_cliente, name="get_coches_cliente"),
    path('get_modelos', views.get_modelos, name="get_modelos"),
    path("mecanico/reparacion/<int:id>", views.reparacion, name="reparacion"),   
    path("agregar_linea/<int:id_reparacion>", views.agregar_linea, name="agregar_linea"),   
    path("recepcion/reparacion/<int:id>", views.reparacion_recepcion, name="reparacion_recepcion"),

]

