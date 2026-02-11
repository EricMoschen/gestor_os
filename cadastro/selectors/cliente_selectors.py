from django.db.models import Count
from cadastro.models import Cliente


def listar_clientes_com_os():

    return (
        Cliente.objects
        .annotate(os_count=Count("ordens_servico"))
        .order_by("codigo")
    )
