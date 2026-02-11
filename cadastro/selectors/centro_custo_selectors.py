from cadastro.models import CentroCusto


def listar_centros_ativos():
    return CentroCusto.objects.filter(ativo=True)


def listar_subcentros(centro):
    return centro.subcentros.filter(ativo=True)


def obter_caminho_hierarquico(centro):

    caminho = [centro.descricao]
    pai = centro.centro_pai

    while pai:
        caminho.append(pai.descricao)
        pai = pai.centro_pai

    return " -> ".join(reversed(caminho))



def listar_centros_raiz():

    return (
        CentroCusto.objects
        .filter(centro_pai__isnull=True)
        .prefetch_related("subcentros__subcentros")
    )
