from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from cadastro.models import Colaborador
from cadastro.services.colaborador_service import alternar_status_colaborador



def alternar_status_colaborador_view(request, pk):

    colaborador = get_object_or_404(Colaborador, pk=pk)

    if request.method == 'POST':
        colaborador = alternar_status_colaborador(colaborador)
        status = "reativado" if colaborador.ativo else "desligado"

        messages.success(
            request,
            f'Colaborador {colaborador.nome} {status} com sucesso!'
        )

    return redirect('cadastro_colaborador')
