from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from abertura_os.models import AberturaOS
from abertura_os.utils.os_pdf import gerar_pdf_imprimir_os


@login_required
def imprimir_os(request, pk):
    ordem_servico = get_object_or_404(AberturaOS, pk=pk)
    pdf_bytes = gerar_pdf_imprimir_os(ordem_servico)

    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'inline; filename="ordem_servico_{ordem_servico.numero_os}.pdf"'
    )
    return response