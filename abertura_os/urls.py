from django.urls import path
from . import views

urlpatterns = [
    path("abertura_os/", views.abrir_os, name="abrir_os"),
    path('imprimir_os/<int:pk>/', views.imprimir_os, name='imprimir_os'),
    path("editar/<int:pk>/", views.editar_os, name="editar_os"),
    path("excluir/<int:pk>/", views.excluir_os, name="excluir_os"),
    path("ajax/subcentros/", views.get_subcentros_ajax, name="get_subcentros"),
    path("finalizar_os/", views.finalizar_os_view, name="finalizar_os"),
    
]

