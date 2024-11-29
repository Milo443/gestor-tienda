"""
URL configuration for tienda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tiendaapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.dashboard, name='dashboard'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('verify_token/<str:email>/', views.verify_token, name='verify_token'),
    path('logout/', views.logout, name='logout'),
    # path('', views.inicio, name='inicio'),

    path('dashboard/', views.dashboard, name='dashboard'),

#gestion de inventario
    path('gestion_inventario/', views.gestion_inventario, name='gestion_inventario'),
    path('form_producto/', views.form_producto, name='form_producto'),
    path('editar_producto/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

#cliente
    path('cliente/', views.cliente, name='cliente'),
    path('form_cliente/', views.form_cliente, name='form_cliente'),
    path('editar_cliente/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar_cliente/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),

#ventas
    path('ventas/', views.ventas, name='ventas'),
    path('form_venta/', views.form_venta, name='form_venta'),
    path('venta_detalle/<int:id>/', views.venta_detalle, name='venta_detalle'),
    path('eliminar_venta/<int:id>/', views.eliminar_venta, name='eliminar_venta'),

#reservas
    path('reservas/', views.reservas, name='reservas'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
