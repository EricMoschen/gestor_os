from src.cadastro.models import Cliente
from django.core.exceptions import ValidationError


def validar_codigo_unico(codigo, cliente_id=None):

    existe = (
        Cliente.objects
        .filter(codigo=codigo)
        .exclude(pk=cliente_id)
        .first()
    )

    if existe:
        raise ValidationError(
            f"Já existe um Cliente com o Código informado: "
            f"{codigo} - {existe.nome}."
        )
