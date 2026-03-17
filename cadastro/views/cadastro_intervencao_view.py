from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from cadastro.models import Intervencao
from cadastro.selectors.intervencao_selectors import listar_intervencoes_com_os
from cadastro.services.intervencao_service import salvar_intervencao, remover_intervencao
from django.core.exceptions import ValidationError


# =============================================================================
# INTERVENÇÕES
# =============================================================================


def cadastro_intervencao(request):
    if request.method == "POST":
        intervencao_id = request.POST.get("intervencao_id")
        descricao = request.POST.get("descricao")

        if not descricao:
            messages.error(request, "Descrição é obrigatória.")
            return redirect("cadastro_intervencao")

        try:
            salvar_intervencao(
                intervencao_id=intervencao_id,
                descricao=descricao,
            )
            messages.success(request, "Intervenção salva com sucesso.")

        except Exception as e:
            messages.error(request, str(e))

        return redirect("cadastro_intervencao")

    intervencoes = listar_intervencoes_com_os()

    context = {
        "intervencoes": intervencoes,
    }

    return render(
        request,
        "cadastro_intervencao/cadastro_intervencao.html",
        context
    )



def excluir_intervencao(request, pk):
    intervencao = get_object_or_404(Intervencao, pk=pk)
    if request.method == "POST":
            try:
                remover_intervencao(intervencao)
                messages.success(request, "Intervenção removida.")
            except ValidationError as e:
                messages.error(request, e.messages[0])

    return redirect("cadastro_intervencao")
