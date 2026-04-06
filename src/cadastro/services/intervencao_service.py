from django.db import transaction
from django.db.models import Max
from django.core.exceptions import ValidationError
from src.cadastro.models import Intervencao


@transaction.atomic
def salvar_intervencao(*, intervencao_id=None, descricao):

    descricao = descricao.strip()

    if not descricao:
        raise ValidationError("Descrição inválida.")

    if intervencao_id:
        interv = Intervencao.objects.select_for_update().get(pk=intervencao_id)
        interv.descricao = descricao
        interv.save()
        return interv

    max_codigo = (
        Intervencao.objects.aggregate(max_codigo=Max("codigo"))
        ["max_codigo"] or 0
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