from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.core.exceptions import ValidationError

from cadastro.forms import CentroCustoForm
from cadastro.models import CentroCusto
from cadastro.selectors.centro_custo_selectors import listar_centros_raiz
from cadastro.services.centro_custo_service import atualizar_centro_custo, criar_centro_custo
from cadastro.services.centro_custo_service import (
    atualizar_centro_custo,
    criar_centro_custo,
    excluir_centro_custo as excluir_centro_custo_service,
)
from cadastro.utils.centro_custo_tree import montar_hierarquia


# =============================================================================
# CENTRO DE CUSTO
# =============================================================================

def cadastrar_centro_custo(request):
    centro = None



    if request.method == "POST":
       centro_id =  request.POST.get("centro_id")
       if centro_id:
          centro = get_object_or_404(CentroCusto, pk=centro_id)

    form = CentroCustoForm(request.POST or None, instance=centro)

    if request.method == 'POST':
        acao = request.POST.get("acao", "salvar")

        if acao == "excluir":
            if centro:
                confirmar_exclusao_filhos = request.POST.get("confirmar_exclusao_filhos") == "1"
                try:
                    filhos_excluidos = excluir_centro_custo_service(
                        centro,
                        confirmar_exclusao_filhos=confirmar_exclusao_filhos,
                    )
                    if filhos_excluidos:
                        messages.success(
                            request,
                            "Centro pai e seus centros filhos foram excluídos com sucesso.",
                        )
                    else:
                        messages.success(request, "Centro de custo excluído com sucesso!")
                except ValidationError as exc:
                    mensagem = exc.messages[0] if getattr(exc, "messages", None) else str(exc)
                    messages.error(request, mensagem)
            else:
                messages.error(request, "Selecione um centro de custos para excluir.")
            return redirect("cadastrar_centro_custo")
        if form.is_valid():
            try:
                if centro:
                    atualizar_centro_custo(centro, **form.cleaned_data)
                    messages.success(request, "Centro de custo atualizado com sucesso.")
                else:
                    criar_centro_custo(**form.cleaned_data)
                    messages.success(request, "Centro de custo cadastrado com suscesso.")
                return redirect("cadastrar_centro_custo")
            except ValidationError as exc:
                fmensagem = exc.messages[0] if getattr(exc, "messages", None) else str(exc)
                form.add_error(None, mensagem)
                messages.error(request, mensagem)

    centros_raiz = listar_centros_raiz()
    hierarquia = montar_hierarquia(centros_raiz)

    context = {
        "form": form,
        "hierarquia": hierarquia,
    }

    return render(request, "cadastro_centro_custo/cadastro_centro_custo.html", context)


def editar_centro_custo(request, id):
   return redirect("cadastrar_centro_custo")

    
def excluir_centro_custo(request, id):
    return redirect("cadastrar_centro_custo")
