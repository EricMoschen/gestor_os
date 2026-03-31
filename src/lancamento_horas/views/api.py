from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from src.cadastro.models import Colaborador
from src.abertura_os.models import AberturaOS



def api_colaborador(request, matricula):
    colaborador = get_object_or_404(Colaborador, matricula__iexact=matricula, ativo=True)
    return JsonResponse({
        "id": colaborador.id,
        "matricula": colaborador.matricula,
        "nome": colaborador.nome,
        "funcao": str(colaborador.funcao) if colaborador.funcao else None,
        "turno": colaborador.turno,
    })



def api_os(request, numero):
    os_obj = get_object_or_404(AberturaOS, numero_os__iexact=numero)
    return JsonResponse({
        "id": os_obj.id,
        "numero_os": os_obj.numero_os,
        "descricao": os_obj.descricao_os,
    })



def api_os_detalhes(request, pk):
    os_obj = get_object_or_404(
        AberturaOS.objects.select_related("centro_custo", "cliente", "motivo_intervencao"),
        pk=pk
    )
    return JsonResponse({
        "id": os_obj.id,
        "numero_os": os_obj.numero_os,
        "descricao_os": os_obj.descricao_os,
        "centro_custo": {
            "id": os_obj.centro_custo.pk if os_obj.centro_custo else None,
            "label": os_obj.centro_custo.descricao if os_obj.centro_custo else "",
        },
        "cliente": os_obj.cliente.pk if os_obj.cliente else None,
        "motivo_intervencao": os_obj.motivo_intervencao.pk if os_obj.motivo_intervencao else None,
        "ssm": os_obj.ssm,
        "situacao": os_obj.situacao,
    })

