

from django.contrib import admin
from django.urls import path, include
from .auth_views import login_view, logout_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("cadastro/", include("cadastro.urls")),
    path("abertura_os/", include("abertura_os.urls")),
    path("lancamento_horas/", include("lancamento_horas.urls")),
    path("relatorios/", include("relatorios.urls")),
]
