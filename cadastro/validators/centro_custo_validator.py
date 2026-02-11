from django.core.exceptions import ValidationError


def validar_hierarquia_circular(centro):

    pai = centro.centro_pai

    while pai:
        if pai == centro:
            raise ValidationError("Hierarquia circular não permitida.")

        pai = pai.centro_pai
