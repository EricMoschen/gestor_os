from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.core.exceptions import ValidationError

from cadastro.forms import CentroCustoForm
from cadastro.models import CentroCusto
from cadastro.selectors.centro_custo_selectors import listar_centros_raiz
from cadastro.services.centro_custo_service import atualizar_centro_custo, criar_centro_custo
from cadastro.utils.centro_custo_tree import montar_hierarquia


# =============================================================================
# CENTRO DE CUSTO
# =============================================================================

def cadastrar_centro_custo(request):
    centro = None



    if request.method == "POST":
       centros_id =  request.POST.get("centros_id")
       if centros_id:
          centro = get_object_or_404(CentroCusto, pk=centros_id)

    form = CentroCustoForm(request.POST or None, instance=centro)

    if request.method == 'POST':
        acao = request.POST.get("acao", "salvar")

        if acao == "excluir":
            if centro:
                centro.delete()
                messages.success(request, "Centro de custo excluído com sucesso!")
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
                form.add_error(None, exc.message)

    centros_raiz = listar_centros_raiz()
    hierarquia = montar_hierarquia(centros_raiz)

    context = {
        "form": form,
        "hierarquia": hierarquia,
    }

    return render(request, "cadastro_centro_custo/cadastro_centro_custo.html", context)


def editar_centro_custo(request, id):
   return redirect("cadastro_centro_custo")

    
def excluir_centro_custo(request, id):
    return redirect("cadastrar_centro_custo")
