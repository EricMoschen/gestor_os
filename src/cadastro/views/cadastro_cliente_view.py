from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages

from src.cadastro.models import Cliente
from src.cadastro.selectors.cliente_selectors import listar_clientes_com_os
from src.cadastro.services.cliente_service import salvar_cliente, remover_cliente


# =============================================================================
# CLIENTES
# =============================================================================

def cadastro_cliente(request):
    if request.method == "POST":
        cliente_id = request.POST.get("cliente_id") or None
        codigo = request.POST.get("codigo")
        nome = request.POST.get("nome")

        if cliente_id:
            cliente_id = int(cliente_id)

        if not codigo or not nome:
            messages.error(request, "Código e Nome são obrigatórios.")
        else:
            try:
                salvar_cliente(
                    cliente_id=cliente_id,
                    codigo=codigo,
                    nome=nome,
                )
                messages.success(request, "Cliente salvo com sucesso.")
                return redirect("cadastro_cliente")

            except ValidationError as e:
                messages.error(request, e.messages[0])

    clientes = listar_clientes_com_os()

    context = {
        "clientes": clientes,
    }

    return render(request, "cadastro_cliente/cadastro_cliente.html", context)



def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        remover_cliente(cliente)
        messages.success(request, "Cliente removido com sucesso.")

    return redirect("cadastro_cliente")
