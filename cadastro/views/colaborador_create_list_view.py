from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from cadastro.forms import ColaboradorForm
from cadastro.selectors.colaborador_selector import listar_colaboradores_com_os
from cadastro.services.colaborador_service import salvar_colaborador




def cadastro_colaborador(request):

    if request.method == 'POST':
        form = ColaboradorForm(request.POST)

        if form.is_valid():
            salvar_colaborador(form)
            messages.success(request, 'Colaborador cadastrado com sucesso!')
            return redirect('cadastro_colaborador')

        messages.error(request, 'Erro ao cadastrar colaborador.')

    else:
        form = ColaboradorForm()

    colaboradores = listar_colaboradores_com_os()

    context = {
        'form': form,
        'colaboradores': colaboradores,
    }

    return render(
        request,
        'cadastro_colaborador/cadastro_colaborador.html',
        context
    )
