from django.urls import path
from . import views

app_name = "lancamento_horas"

urlpatterns = [
    path("apontar/", views.apontar_horas, name="apontar_horas"),
    path("api/colaborador/<str:matricula>/", views.api_colaborador, name="api_colaborador"),
    path("api/os/<str:numero>/", views.api_os, name="api_os"),
    path("api/os/<int:pk>/detalhes/", views.api_os_detalhes, name="api_os_detalhes"),
    path("ajuste/", views.ajuste_horas, name="ajuste_horas"),
]
