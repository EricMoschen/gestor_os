from cadastro.models import CentroCusto
from cadastro.validators.centro_custo_validator import validar_hierarquia_circular


def criar_centro_custo(**dados):

    centro = CentroCusto(**dados)

    validar_hierarquia_circular(centro)

    centro.save()

    return centro


def atualizar_centro_custo(centro, **dados):

    for campo, valor in dados.items():
        setattr(centro, campo, valor)

    validar_hierarquia_circular(centro)

    centro.save()

    return centro
