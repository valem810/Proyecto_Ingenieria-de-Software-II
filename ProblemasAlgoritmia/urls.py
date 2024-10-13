"""
URL configuration for ProblemasAlgoritmia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from AlgoritmiaApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('resolver_tablero/', views.resolver_tablero, name='resolver_tablero'),
    path('resolver_reinas/', views.resolver_reinas, name='resolver_reinas'),
    path('generar_pdf/<int:n>/', views.generar_pdf, name='generar_pdf'),
    path('resolver_reinas/', views.resolver_reinas, name='resolver_reinas'),
    path('generar_pdf_reinas/', views.generar_pdf_reinas, name='generar_pdf_reinas'),
    path('cargar_archivo/', views.cargar_archivo_view, name='cargar_archivo'),
    path('descargar_pdf/', views.descargar_pdf_view, name='descargar_pdf'),
    path('descargar/', views.descargar_archivo_view, name='descargar_archivo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
