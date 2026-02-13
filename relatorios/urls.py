from django.urls import path
from .views import (
    relatorio_os,
    orcamento_pdf,
    proximo_orcamento,
    log_os,
    log_os_pdf,
)

urlpatterns = [
    path("", relatorio_os, name="relatorio_os"),
    path("orcamento-pdf/", orcamento_pdf, name="orcamento_pdf"),
    path("proximo-orcamento/", proximo_orcamento, name="proximo_orcamento"),
    path("log/<str:numero_os>/", log_os, name="log_os"),
    path("log/<str:numero_os>/pdf/", log_os_pdf, name="log_os_pdf"),
]
