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

    # Rota para Cadastro de Colaboradores    
    path('colaborador/', views.cadastro_colaborador, name='cadastro_colaborador'),
    path('editar/<int:pk>/', views.editar_colaborador, name='editar_colaborador'),
    path('excluir/<int:pk>/', views.excluir_colaborador, name='excluir_colaborador'),

    # Rota para Cadastro de Funções
    path("funcoes/", views.cadastro_funcao, name="cadastro_funcao"),
    path("funcoes/editar/<int:id>/", views.editar_funcao, name="editar_funcao"),
    path("funcoes/excluir/<int:id>/", views.excluir_funcao, name="excluir_funcao"),
]

