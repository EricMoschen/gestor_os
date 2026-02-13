from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def dashboard(request):

    cards = [
        {
            "title": "Centro de Custos",
            "url": "cadastrar_centro_custo",
            "color": "color-purple",
        },
        {
            "title": "Clientes",
            "url": "cadastro_cliente",
            "color": "color-yellow",
        },
        {
            "title": "Intervenção",
            "url": "cadastro_intervencao",
            "color": "color-blue",
        },
        {
            "title": "Colaborador",
            "url": "cadastro_colaborador",
            "color": "color-blue",
        },
        {
            "title": "Abrir OS",
            "url": "abrir_os",
            "color": "color-blue",
        },
        {
            "title": "Apontar Horas",
            "url": "lancamento_horas:apontar_horas",
            "color": "color-blue",
        },
        {
            "title": "Ajustar Horas",
            "url": "lancamento_horas:ajuste_horas_supervisor",
            "color": "color-blue",
        },
        {
            "title": "Finalizar OS",
            "url": "finalizar_os",
            "color": "color-blue",
        },
        
    ]

    return render(request, "dashboard.html", {"cards": cards})
