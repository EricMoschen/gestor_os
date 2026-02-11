from django.db.models import Count
from cadastro.models import Intervencao


def listar_intervencoes_com_os():
    return (
        Intervencao.objects
        .annotate(os_count=Count("aberturaos", distinct=True))
        .order_by("codigo")
    )
