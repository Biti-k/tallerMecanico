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
    path("eliminar_linea/<int:id_linea>", views.eliminar_linea, name="eliminar_linea"),   
    path("recepcion/reparacion/<int:id>", views.reparacion_recepcion, name="reparacion_recepcion"),
    path("recepcion/facturar_reparacion/<int:id>", views.facturar_reparacion, name="facturar_reparacion"),
    path("recepcion/modificar_linea/<int:id>", views.modificar_linea_recepcion, name="modificar_linea_recepcion"),
    path("recepcion/facturas", views.facturas, name="facturas"),
    path("mecanico/modificar_linea/<int:id>", views.modificar_linea_mecanico, name="modificar_linea_mecanico"),
    path("mecanico/rechazar_reparacion/<int:id_reparacion>", views.rechazar_reparacion, name="rechazar_reparacion"),
    path("mecanico/cerrar_reparacion/<int:id_reparacion>", views.cerrar_reparacion, name="cerrar_reparacion"),
    path("logout", views.logout_view, name="logout"),
]

