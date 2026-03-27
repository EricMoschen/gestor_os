from cadastro.models import CentroCusto


def listar_centros_ativos(tenant_id="default"):
    return CentroCusto.objects.filter(ativo=True, tenant_id=tenant_id)


def listar_subcentros(tag):
    return tag.subtags.filter(ativo=True)


def obter_caminho_hierarquico(tag):
    caminho = [tag.descricao]
    pai = tag.tag_pai

    while pai:
        caminho.append(pai.descricao)
        pai = pai.tag_pai

    return " -> ".join(reversed(caminho))

def listar_centros_raiz(tenant_id="default"):
    return (
        CentroCusto.objects.filter(tag_pai__isnull=True, tenant_id=tenant_id).prefetch_related("subtags__subtags")
    )
