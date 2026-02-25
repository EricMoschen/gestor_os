from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import datetime, time
from importlib.util import find_spec
from importlib import import_module


from ..utils.relatorio import (construir_contexto_relatorio_os,processar_relatorio,montar_dados_log_os)
from ..utils.orcamento import gerar_proximo_orcamento
from abertura_os.models import AberturaOS
from lancamento_horas.models import ApontamentoHoras


def relatorio_os(request):
    context = construir_contexto_relatorio_os(request)
    return render(request, "relatorios/menu_relatorios.html", context)



def orcamento_pdf(request):
    context = construir_contexto_relatorio_os(request)
    
    os_obj = context.get("os_detalhe")
    data_inicio = context.get("data_inicio")
    data_fim = context.get("data_fim")

    dados_log = []
    total_log = None

    if os_obj: 
        dados_log, total_log = montar_dados_log_os(
            os_obj,
            data_inicio = data_inicio,
            data_fim = data_fim,
        )

    context.update({ 
       "dados_log": dados_log,
       "total_log": total_log,
       "numero_orcamento":str(gerar_proximo_orcamento()).zfill(4),
       "data_emissao": timezone.now().strftime("%d/%m/%y"),
    })

    return render(request, "relatorios/orcamento_horas_pdf.html", context)



def proximo_orcamento(request):
    return JsonResponse({"numero": str(gerar_proximo_orcamento()).zfill(4)})



def log_os(request, numero_os):
    os_obj = get_object_or_404(AberturaOS, numero_os=numero_os)
    data_inicio = parse_date(request.GET.get("data_inicio") or "")
    data_fim = parse_date(request.GET.get("data_fim") or "")

    apontamentos = ApontamentoHoras.objects.select_related(
        "colaborador__funcao"
    ).filter(ordem_servico=os_obj)

    if data_inicio:
        apontamentos = apontamentos.filter(
            data_fim__gte=datetime.combine(data_inicio, time.min)
        )

    if data_fim:
        apontamentos = apontamentos.filter(
            data_inicio__lte=datetime.combine(data_fim, time.max)
        )

    relatorio, totais = ([], None)

    if apontamentos.exists():
        relatorio, totais = processar_relatorio(apontamentos)

    # 👇 CHAMANDO SUA FUNÇÃO AQUI
    dados_log, total_log = montar_dados_log_os(
        os_obj,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

    return render(request, "relatorios/orcamento_horas_pdf.html", {
        "os_detalhes": os_obj,
        "relatorio": relatorio,
        "totais": totais,
        "dados_log": dados_log,          # 👈 enviando para o template
        "total_log": total_log,          # 👈 enviando total formatado
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "numero_orcamento": str(gerar_proximo_orcamento()).zfill(4),
        "data_emissao": timezone.now().strftime("%d/%m/%y"),
    })

def log_os_pdf(request, numero_os):
    os_obj = get_object_or_404(AberturaOS, numero_os=numero_os)

    data_inicio = parse_date(request.GET.get("data_inicio") or "")
    data_fim = parse_date(request.GET.get("data_fim") or "")

    apontamentos = (
        ApontamentoHoras.objects
        .select_related("colaborador__funcao")
        .filter(ordem_servico=os_obj)
    )

    if data_inicio:
        apontamentos = apontamentos.filter(
            data_fim__gte=datetime.combine(data_inicio, time.min)
        )

    if data_fim:
        apontamentos = apontamentos.filter(
            data_inicio__lte=datetime.combine(data_fim, time.max)
        )

    relatorio, totais = ([], None)

    if apontamentos.exists():
        relatorio, totais = processar_relatorio(apontamentos)

    context = {
        "os_detalhes": os_obj,
        "relatorio": relatorio,
        "totais": totais,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "numero_orcamento": str(gerar_proximo_orcamento()).zfill(4),
        "data_emissao": timezone.now().strftime("%d/%m/%y"),
    }

    return render(request, "relatorios/orcamento_cliente_pdf.html", context)