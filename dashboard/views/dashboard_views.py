from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def dashboard(request):

    categorias = [

        {
            "nome": "Ordens de Serviço",
            "cards": [
                {
                    "title": "Abrir OS",
                    "url": "abrir_os",
                    "color": "color-purple",
                },
                {
                    "title": "Apontar Horas",
                    "url": "lancamento_horas:apontar_horas",
                    "color": "color-purple",
                },
                {
                    "title": "Ajustar Horas",
                    "url": "lancamento_horas:ajuste_horas",
                    "color": "color-purple",
                },
                {
                    "title": "Finalizar OS",
                    "url": "finalizar_os",
                    "color": "color-purple",
                },
            ]
        },

        {
            "nome": "Cadastros",
            "cards": [
                {
                    "title": "Centro de Custos",
                    "url": "cadastrar_centro_custo",
                    "color": "color-pink",
                },
                {
                    "title": "Clientes",
                    "url": "cadastro_cliente",
                    "color": "color-pink",
                },
                {
                    "title": "Intervenção",
                    "url": "cadastro_intervencao",
                    "color": "color-pink",
                },
                {
                    "title": "Colaborador",
                    "url": "cadastro_colaborador",
                    "color": "color-pink",
                },
                {
                    "title": "Função",
                    "url": "cadastro_funcao",
                    "color": "color-pink",
                },
            ]
        },

        

        {
            "nome": "Relatórios",
            "cards": [
                {
                    "title": "Relatórios",
                    "url": "relatorio_os",
                    "color": "color-red",
                }
            ]
        }
    ]


    return render(request, "dashboard.html", {"categorias": categorias})

