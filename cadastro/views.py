from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from cadastro.forms import CentroCustoForm
from cadastro.models import Cliente

from cadastro.selectors.centro_custo_selectors import listar_centros_raiz
from cadastro.selectors.cliente_selectors import listar_clientes_com_os

from cadastro.services.centro_custo_service import criar_centro_custo
from cadastro.services.cliente_service import salvar_cliente, remover_cliente

from cadastro.utils.centro_custo_tree import montar_hierarquia


# =================================================================================
# CENTRO DE CUSTO
# =================================================================================


def cadastrar_centro_custo(request):

    form = CentroCustoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        criar_centro_custo(**form.cleaned_data)
        return redirect("cadastrar_centro_custo")

    centros_raiz = listar_centros_raiz()
    hierarquia = montar_hierarquia(centros_raiz)

    return render(
        request,
        "cadastro_centro_custo/cadastro_centro_custo.html",
        {
            "form": form,
            "hierarquia": hierarquia,
        }
    )


# =================================================================================
# CLIENTES
# =================================================================================


def cadastro_cliente(request):

    mensagem_erro = None

    if request.method == "POST":

        cliente_id = request.POST.get("cliente_id") or None
        codigo = request.POST.get("codigo")
        nome = request.POST.get("nome")

        if cliente_id:
            cliente_id = int(cliente_id)

        if not codigo or not nome:
            mensagem_erro = "Código e Nome são obrigatórios."
        else:
            try:
                salvar_cliente(
                    cliente_id=cliente_id,
                    codigo=codigo,
                    nome=nome
                )
                return redirect("cadastro_cliente")

            except ValidationError as e:
                mensagem_erro = e.messages[0]

    clientes = listar_clientes_com_os()

    return render(
        request,
        "cadastro_cliente/cadastro_cliente.html",
        {
            "clientes": clientes,
            "mensagem_erro": mensagem_erro,
        }
    )


@login_required
def excluir_cliente(request, pk):

    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        remover_cliente(cliente)
        return redirect("cadastro_cliente")

    return redirect("cadastro_cliente")
