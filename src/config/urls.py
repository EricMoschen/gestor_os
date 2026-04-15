

from django.contrib import admin
from django.urls import path, include
from .auth_views import login_view, logout_view, update_theme_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("preferencias/tema/", update_theme_view, name="update_theme"),
    path("admin/", admin.site.urls),
    path("", include("src.dashboard.urls")),
    path("cadastro/", include("src.cadastro.urls")),
    path("abertura_os/", include("src.abertura_os.urls")),
    path("lancamento_horas/", include("src.lancamento_horas.urls")),
    path("relatorios/", include("src.relatorios.urls")),
]
