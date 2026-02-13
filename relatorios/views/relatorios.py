from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone


from ..utils.relatorio import (construir_contexto_relatorio_os,montar_dados_log_os)
from ..utils.orcamento import gerar_proximo_orcamento
from abertura_os.models import AberturaOS





def relatorio_os(request):
    context = construir_contexto_relatorio_os(request)
    return render(request, "relatorios/menu_relatorios.html", context)



def orcamento_pdf(request):
    context = construir_contexto_relatorio_os(request)
    return render(request, "relatorios/orcamento_horas_pdf.html", context)



def proximo_orcamento(request):
    return JsonResponse({"numero": str(gerar_proximo_orcamento()).zfill(4)})



def log_os(request, numero_os):
    os_obj = get_object_or_404(AberturaOS, numero_os=numero_os)
    dados, total_horas = montar_dados_log_os(os_obj)
    return render(request, "relatorios/orcamento_cliente_pdf.html", {
        "os": os_obj,
        "dados": dados,
        "total_horas": total_horas,
        "data_emissao": timezone.now().strftime("%d/%m/%Y %H:%M")
    })


def log_os_pdf(request, numero_os):
    os_obj = get_object_or_404(AberturaOS, numero_os=numero_os)
    dados, total_horas = montar_dados_log_os(os_obj)
    html = render_to_string("relatorios/orcamento_cliente_pdf.html", {
        "logo_path": request.build_absolute_uri("/static/img/logo.png"),
        "data_emissao": timezone.now().strftime("%d/%m/%Y %H:%M"),
        "os": os_obj,
        "dados": dados,
        "total_horas": total_horas,
    })
    pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()
    return HttpResponse(pdf, content_type="application/pdf")
