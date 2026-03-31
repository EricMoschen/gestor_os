from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from src.abertura_os.models import AberturaOS
from src.abertura_os.forms import AberturaOSForm
from src.abertura_os.services.abertura_os_service import AberturaOSService
from src.abertura_os.queries.centro_custo_queries import get_centros_pais



def editar_os(request, pk):

    os_instance = get_object_or_404(AberturaOS, pk=pk)

    if request.method == "POST":
        form = AberturaOSForm(request.POST, instance=os_instance)

        if form.is_valid():
            try:
                AberturaOSService.atualizar_os(
                    form=form,
                    centro_id=request.POST.get("centro_custo")
                )
                messages.success(request, "OS atualizada com sucesso!")
                return redirect("abrir_os")
            except ValueError as erro:
                form.add_error(None, str(erro))

    else:
        form = AberturaOSForm(instance=os_instance)

    context = {
        "form": form,
        "proximo_numero": os_instance.numero_os,
        "ordens": AberturaOSService.listar_ordens(),
        "pais_centro_custo": get_centros_pais(),
        "modo_edicao": True,
        "os_id": os_instance.id,
        "selected_centro_label": (
            os_instance.centro_custo.descricao
            if os_instance.centro_custo else ""
        ),
    }

    return render(request, "abertura_os/abertura_os.html", context)
