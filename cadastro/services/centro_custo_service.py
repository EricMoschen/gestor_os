from django.db import transaction
from django.core.exceptions import ValidationError

from abertura_os.models import AberturaOS
from cadastro.models import CentroCusto
from cadastro.validators.centro_custo_validator import validar_hierarquia_circular


def criar_centro_custo(**dados):

    centro = CentroCusto(**dados)

    validar_hierarquia_circular(centro)

    centro.save()

    return centro


def atualizar_centro_custo(centro, **dados):

    codigo_atual = centro.cod_centro
    novo_codigo = dados.get("cod_centro", codigo_atual)

    for campo, valor in dados.items():
        setattr(centro, campo, valor)

    validar_hierarquia_circular(centro)

    if novo_codigo == codigo_atual:
        centro.save()
        return centro

    with transaction.atomic():
        centro_atualizado = CentroCusto.objects.create(
            cod_centro = novo_codigo,
            descricao = centro.descricao,
            centro_pai = centro.centro_pai,
            ativo = centro.ativo,
        )

        CentroCusto.objects.filter(centro_pai_id=codigo_atual).update(cento_pai=centro_atualizado)
        AberturaOS.objects.filter(centro_custo_id=codigo_atual).update(centro_custo=centro_atualizado)

        centro.delete()
    
    return(centro_atualizado)


def _listar_descendentes(centro):
    descendentes = []
    fila = list(centro.subcentros.all())

    while fila:
        atual = fila.pop(0)
        descendentes.append(atual)
        fila.extend(atual.subcentros.all())

    return descendentes


def excluir_centro_custo(centro, confirmar_exclusao_filhos=False):
    descendentes = _listar_descendentes(centro)
    centros_para_excluir = [centro, *descendentes]

    os_vinculadas = (
        AberturaOS.objects
        .filter(centro_custo__in=centros_para_excluir)
        .values_list("centro_custo__descricao", flat=True)
        .distinct()
    )

    centros_com_os = list(os_vinculadas)
    if centros_com_os:
        raise ValidationError(
            "Não é possível excluir. O centro de custo está em uso em alguma OS: "
            + ", ".join(centros_com_os)
            + "."
        )

    if descendentes and not confirmar_exclusao_filhos:
        nomes_filhos = ", ".join(filho.descricao for filho in descendentes)
        raise ValidationError(
            "Este centro pai possui centros filhos: "
            + nomes_filhos
            + ". Confirme a exclusão para remover todos."
        )

    CentroCusto.objects.filter(pk__in=[item.pk for item in centros_para_excluir]).delete()
    return descendentes