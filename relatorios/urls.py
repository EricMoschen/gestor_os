from django.urls import path
from config.access_control import ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE, ROLE_SUPERVISOR, role_required
from .views import (
    log_os,
    log_os_pdf,
    orcamento_pdf,
    proximo_orcamento,
    relatorio_os,
)

urlpatterns = [
    path("",role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (relatorio_os), name="relatorio_os"),
    path("orcamento-pdf/",role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (orcamento_pdf), name="orcamento_pdf"),
    path("proximo-orcamento/",role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (proximo_orcamento), name="proximo_orcamento"),
    path("log/<str:numero_os>/",role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (log_os), name="log_os"),
    path("log/<str:numero_os>/pdf/",role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (log_os_pdf), name="log_os_pdf"),
]
