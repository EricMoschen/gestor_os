from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.deletion import ProtectedError

from abertura_os.models import AberturaOS
from cadastro.models import CentroCusto
from cadastro.validators.centro_custo_validator import validar_hierarquia_circular


def criar_centro_custo(**dados):
    dados.setdefault("tenait_id", "default")
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


def _listar_descendentes(centro):
    descendentes = []
    fila = list(centro.subtags.all())

    while fila:
        atual = fila.pop(0)
        descendentes.append(atual)
        fila.extend(atual.subtags.all())

    return descendentes


def excluir_centro_custo(centro, confirmar_exclusao_filhos=False):
    descendentes = _listar_descendentes(centro)
    centros_para_excluir = [centro, *descendentes]

    os_vinculadas = (
       AberturaOS.objects.filter(centro_custo__in=centros_para_excluir)
        .values_list("centro_custo__descricao", flat=True)
        .distinct()
    )

    centros_com_os = list(os_vinculadas)
    if centros_com_os:
       raise ValidationError(
            "Não é possível excluir. O ativo está em uso em alguma OS: " + ", ".join(centros_com_os) + "."
        )
    
    try:
        with transaction.atomic():
            for descendente in reversed(descendentes):
                descendente.delete()
            centro.delete()
    except ProtectedError:
        raise ValidationError("Não é possível excluir. O ativo está em uso em alguma OS.")

    return descendentes