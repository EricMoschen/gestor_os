from django.urls import path
from config.access_control import ROLE_ADM, ROLE_PCM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE, role_required
from . import views

app_name = "lancamento_horas"

urlpatterns = [
    path("apontar/", role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (views.apontar_horas), name="apontar_horas"),
    path("api/colaborador/<str:matricula>/",role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (views.api_colaborador), name="api_colaborador"),
    path("api/os/<str:numero>/",role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (views.api_os), name="api_os"),
    path("api/os/<int:pk>/detalhes/",role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (views.api_os_detalhes), name="api_os_detalhes"),
    path("ajuste/", role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (views.ajuste_horas), name="ajuste_horas"),
]
