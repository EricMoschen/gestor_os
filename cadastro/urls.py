from django.urls import path
from config.access_control import (
    ROLE_ADM,
    ROLE_ALMOXARIFE,
    ROLE_PCM,
    ROLE_SUPERVISOR,
    role_required,
    )

from . import views

urlpatterns = [
    # Rota Centro de Custos
    path("centro-custo/",role_required([ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE]) (views.cadastrar_centro_custo), name="cadastrar_centro_custo"),
    path("centro-custo/editar/<int:id>/",role_required([ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE]) (views.editar_centro_custo), name="editar_centro_custo"),
    path("centro-custo/excluir/<int:id>/",role_required([ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE]) (views.excluir_centro_custo), name="excluir_centro_custo"),

    # Rota Clientes
    path("cliente/",role_required([ROLE_ADM, ROLE_ALMOXARIFE])(views.cadastro_cliente), name="cadastro_cliente"),
    path("cliente/excluir/<int:pk>/",role_required([ROLE_ADM, ROLE_ALMOXARIFE])(views.excluir_cliente), name="excluir_cliente"),

    # Rota para Intervenções
    path('intervencao/',role_required([ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE]) (views.cadastro_intervencao), name='cadastro_intervencao'),
    path('intervencao/excluir/<int:pk>/',role_required([ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE]) (views.excluir_intervencao), name='excluir_intervencao'),

    # Rota para Cadastro de Colaboradores    
    path('colaborador/',role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (views.cadastro_colaborador), name='cadastro_colaborador'),
    path('editar/<int:pk>/',role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (views.editar_colaborador), name='editar_colaborador'),
    path('excluir/<int:pk>/',role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (views.excluir_colaborador), name='excluir_colaborador'),

    # Rota para Cadastro de Funções
    path("funcoes/",role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (views.cadastro_funcao), name="cadastro_funcao"),
    path("funcoes/editar/<int:id>/",role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (views.editar_funcao), name="editar_funcao"),
    path("funcoes/excluir/<int:id>/",role_required([ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]) (views.excluir_funcao), name="excluir_funcao"),
]

