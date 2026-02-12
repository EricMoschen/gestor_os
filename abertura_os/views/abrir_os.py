from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..models import AberturaOS
from ..forms import AberturaOSForm
from ..services.abertura_os_service import AberturaOSService
from ..queries.centro_custo_queries import get_centros_pais



def abrir_os(request):

    # Preview do próximo número (não salva ainda)
    preview_numero = AberturaOS.gerar_proximo_numero_os()

    if request.method == "POST":
        form = AberturaOSForm(request.POST)

        if form.is_valid():
            try:
                AberturaOSService.criar_os(
                    form=form,
                    centro_id=request.POST.get("centro_custo")
                )
                messages.success(request, "OS criada com sucesso!")
                return redirect("abrir_os")

            except ValueError as erro:
                form.add_error(None, str(erro))

    else:
        form = AberturaOSForm()

    context = {
        "form": form,
        "proximo_numero": preview_numero,  # Somente para mostrar na tela
        "ordens": AberturaOSService.listar_ordens(),
        "pais_centro_custo": get_centros_pais(),
        "modo_edicao": False,
    }

    return render(request, "abertura_os/abertura_os.html", context)
