from django.db import transaction
from django.db.models import Max
from django.core.exceptions import ValidationError
from cadastro.models import Intervencao


@transaction.atomic
def salvar_intervencao(*, intervencao_id=None, descricao):

    descricao = descricao.strip()

    if not descricao:
        raise ValidationError("Descrição inválida.")

    # ========================
    # EDITAR
    # ========================
    if intervencao_id:
        interv = Intervencao.objects.select_for_update().get(
            codigo=intervencao_id
        )

        interv.descricao = descricao
        interv.save()

        return interv

    # ========================
    # CRIAR
    # ========================
    max_codigo = (
        Intervencao.objects.select_for_update()
        .aggregate(max_codigo=Max("codigo"))
        ["max_codigo"]
        or 0
    )

    return Intervencao.objects.create(
        codigo=max_codigo + 1,
        descricao=descricao
    )
    
def remover_intervencao(intervencao):

    if intervencao.aberturaos.exists():
        raise ValidationError(
            "Não é possível excluir. Intervenção está vinculada a OS."
        )

    intervencao.delete()