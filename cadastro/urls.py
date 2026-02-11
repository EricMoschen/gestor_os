from django.urls import path
from . import views

urlpatterns = [
    # Rota Centro de Custos
    path("centro-custo/", views.cadastrar_centro_custo, name="cadastrar_centro_custo"),

    # Rota Clientes
    path("cliente/", views.cadastro_cliente, name="cadastro_cliente"),
    path("cliente/excluir/<int:pk>/", views.excluir_cliente, name="excluir_cliente"),

    # Rota para Intervenções
    path('intervencao/', views.cadastro_intervencao, name='cadastro_intervencao'),
    path('intervencao/excluir/<int:pk>/', views.excluir_intervencao, name='excluir_intervencao'),
]

