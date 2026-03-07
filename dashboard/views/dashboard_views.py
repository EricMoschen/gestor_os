from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from config.access_control import (
    ROLE_ADM,
    ROLE_PCM,
    ROLE_SUPERVISOR,
    ROLE_ALMOXARIFE,
    ensure_roles_exist,
    user_has_any_role,
)

@login_required
def dashboard(request):

    ensure_roles_exist()

    categorias = [
        {
            "nome": "Ordens de Serviço",
            "cards": [
                {
                    "title": "Abrir OS",
                    "url": "abrir_os",
                    "color": "color-purple",
                    "roles": [ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE],
                },
                {
                    "title": "Apontar Horas",
                    "url": "lancamento_horas:apontar_horas",
                    "color": "color-purple",
                    "roles": [ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE],
                },
                {
                    "title": "Ajustar Horas",
                    "url": "lancamento_horas:ajuste_horas",
                    "color": "color-purple",
                    "roles": [ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE],
                },
                {
                    "title": "Finalizar OS",
                    "url": "finalizar_os",
                    "color": "color-purple",
                    "roles": [ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE],
                },
            ],
        },

        {
            "nome": "Cadastros",
            "cards": [
                {
                    "title": "Centro de Custos",
                    "url": "cadastrar_centro_custo",
                    "color": "color-pink",
                    "roles": [ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE],
                },
                {
                    "title": "Clientes",
                    "url": "cadastro_cliente",
                    "color": "color-pink",
                    "roles": [ROLE_ADM, ROLE_ALMOXARIFE],
                },
                {
                    "title": "Intervenção",
                    "url": "cadastro_intervencao",
                    "color": "color-pink",
                    "roles": [ROLE_ADM, ROLE_PCM, ROLE_ALMOXARIFE],
                },
                {
                    "title": "Colaborador",
                    "url": "cadastro_colaborador",
                    "color": "color-pink",
                    "roles": [ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE],
                },
                {
                    "title": "Função",
                    "url": "cadastro_funcao",
                    "color": "color-pink",
                    "roles": [ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE],
                },
            ],
        },

        

        {
            "nome": "Relatórios",
            "cards": [
                {
                    "title": "Relatórios",
                    "url": "relatorio_os",
                    "color": "color-red",
                    "roles": [ROLE_ADM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE],
                }
            ],
        },
    ]

    for categoria in categorias:
        categoria["cards"] = [
            card for card in categoria["cards"] if user_has_any_role(request.user, card["roles"])
        ]

        categorias = [categoria for categoria in categorias if categoria["cards"]]


    return render(request, "dashboard.html", {"categorias": categorias})

