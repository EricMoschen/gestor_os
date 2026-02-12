

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls")),
    path("cadastro/", include("cadastro.urls")),
    path("abertura_os/", include("abertura_os.urls")),
]
