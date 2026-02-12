from django.db.models import Count
from cadastro.models import Colaborador



def listar_colaboradores_com_os():
    return (
        Colaborador.objects
        .annotate(os_count=Count('apontamentohoras'))
        .order_by('nome')
    )


def listar_colaboradores():
    return Colaborador.objects.order_by('nome')
