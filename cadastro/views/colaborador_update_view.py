from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from cadastro.forms import ColaboradorForm
from cadastro.models import Colaborador
from cadastro.selectors.colaborador_selector import listar_colaboradores
from cadastro.services.colaborador_service import salvar_colaborador



def editar_colaborador(request, pk):

    colaborador = get_object_or_404(Colaborador, pk=pk)

    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador, include_status=True)

        if form.is_valid():
            salvar_colaborador(form)
            messages.success(
                request,
                f'Colaborador {colaborador.nome} atualizado com sucesso!'
            )
            return redirect('cadastro_colaborador')

        messages.error(request, 'Erro ao atualizar colaborador.')

    else:
        form = ColaboradorForm(instance=colaborador, include_status=True)

    colaboradores = listar_colaboradores()

    context = {
        'form': form,
        'colaboradores': colaboradores,
        'editando': True,
        'colaborador_editando': colaborador
    }

    return render(
        request,
        'cadastro_colaborador/cadastro_colaborador.html',
        context
    )
