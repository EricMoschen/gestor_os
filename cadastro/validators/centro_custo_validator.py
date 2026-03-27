from django.core.exceptions import ValidationError


def validar_hierarquia_circular(tag):
    pai = tag.tag_pai

    while pai:
        if pai == tag:
            raise ValidationError("Hierarquia circular não permitida.")

        pai = pai.tag_pai