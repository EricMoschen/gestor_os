from django.db import transaction

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