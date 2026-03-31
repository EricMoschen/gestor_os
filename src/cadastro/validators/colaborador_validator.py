from django.core.exceptions import ValidationError
from src.cadastro.models.choices import TurnoChoices


def validar_horarios_outros(colaborador):
    """
    Garante preenchimento completo quando turno = OUTROS
    """

    if colaborador.turno == TurnoChoices.OUTROS:
        campos = [
            colaborador.hr_entrada_am,
            colaborador.hr_saida_am,
            colaborador.hr_entrada_pm,
            colaborador.hr_saida_pm
        ]

        if not all(campos):
            raise ValidationError(
                "Para turno 'Outros', todos os horários devem ser informados."
            )
