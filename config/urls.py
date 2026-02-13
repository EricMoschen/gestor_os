

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("cadastro/", include("cadastro.urls")),
    path("abertura_os/", include("abertura_os.urls")),
    path("lancamento_horas/", include("lancamento_horas.urls")),
]
