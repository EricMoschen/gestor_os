from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from cadastro.models import Colaborador
from cadastro.services.colaborador_service import deletar_colaborador



def excluir_colaborador(request, pk):

    colaborador = get_object_or_404(Colaborador, pk=pk)

    if request.method == 'POST':
        nome = deletar_colaborador(colaborador)

        messages.success(
            request,
            f'Colaborador {nome} excluído com sucesso!'
        )

    return redirect('cadastro_colaborador')
