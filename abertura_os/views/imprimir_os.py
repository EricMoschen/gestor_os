from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from abertura_os.models import AberturaOS

@login_required
def imprimir_os(request, pk):
    ordem_servico = get_object_or_404(
        AberturaOS.objects.select_related("centro_custo", "cliente", "motivo_intervencao"),
        pk=pk,
    )
    template_name = (
        "imprimir_os/imprimir_os_docx.html"
        if request.GET.get("editavel") == "1"
        else "imprimir_os/imprimir_os.html"
    )
    return render(
        request,
        template_name,
        {
            "os": ordem_servico,
        },
    )