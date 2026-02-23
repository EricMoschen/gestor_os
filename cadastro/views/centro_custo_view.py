from django.shortcuts import render, redirect
from django.contrib import messages

from cadastro.forms import CentroCustoForm
from cadastro.selectors.centro_custo_selectors import listar_centros_raiz
from cadastro.services.centro_custo_service import criar_centro_custo
from cadastro.utils.centro_custo_tree import montar_hierarquia


# =============================================================================
# CENTRO DE CUSTO
# =============================================================================

def cadastrar_centro_custo(request):
    form = CentroCustoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        criar_centro_custo(**form.cleaned_data)
        messages.success(request, "Centro de custo cadastrado com sucesso!")
        return redirect("cadastrar_centro_custo")

    centros_raiz = listar_centros_raiz()
    hierarquia = montar_hierarquia(centros_raiz)

    context = {
        "form": form,
        "hierarquia": hierarquia,
    }

    return render(request, "cadastro_centro_custo/cadastro_centro_custo.html", context)




def editar_centro_custo(request, id):
    centro = get_object_or_404(CentroCusto, id=id)
    form = CentroCustoForm(request.POST or None, instance=centro)

    if request.method == "POST" and form.is_valid():
        atualizar_centro_custo(centro, **form.cleaned_data)
        messages.success(request, "Centro de custo atualizado com sucesso!")
        return redirect("cadastrar_centro_custo")

    centros_raiz = listar_centros_raiz()
    hierarquia = montar_hierarquia(centros_raiz)

    context = {
        "form": form,
        "hierarquia": hierarquia,
        "editar": True,
        "centro": centro
    }

    return render(request, "cadastro_centro_custo/cadastro_centro_custo.html", context)



    
def excluir_centro_custo(request, id):
    centro = get_object_or_404(CentroCusto, id=id)

    if request.method == "POST":
        centro.delete()
        messages.success(request, "Centro de custo excluído com sucesso!")
        return redirect("cadastrar_centro_custo")

    # Caso queira confirmar exclusão via GET (opcional)
    return render(request, "cadastro_centro_custo/confirmar_exclusao.html", {"centro": centro})