from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from cadastro.forms import CentroCustoForm
from cadastro.selectors.centro_custo_selectors import listar_centros_raiz
from cadastro.services.centro_custo_service import criar_centro_custo
from cadastro.utils.centro_custo_tree import montar_hierarquia


from .forms import CentroCustoForm


def cadastrar_centro_custo(request):

    form = CentroCustoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        criar_centro_custo(**form.cleaned_data)
        return redirect("cadastrar_centro_custo")

    centros_raiz = listar_centros_raiz()
    hierarquia = montar_hierarquia(centros_raiz)

    context = {
        "form": form,
        "hierarquia": hierarquia,
    }

    return render(
        request,
        "cadastro_centro_custo/cadastro_centro_custo.html",
        context
    )
