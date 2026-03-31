from django.db.models import Count
from src.cadastro.models import Colaborador, Funcao_colab



def listar_colaboradores_com_os():
    return (
        Colaborador.objects
        .annotate(os_count=Count('apontamentohoras'))
        .order_by('nome')
    )


def listar_colaboradores():
    return Colaborador.objects.order_by('nome')

def listar_funcoes_com_colaboradores():
    return(
        Funcao_colab.objects
        .annotate(colaboradores_count=Count("Função_Colaborador"))
        .order_by("descricao")
)