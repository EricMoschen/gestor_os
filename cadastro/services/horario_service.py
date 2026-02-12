from datetime import time
from cadastro.models.choices import TurnoChoices


class HorarioService:

    @staticmethod
    def horario_inicio(turno, entrada_personalizada):
        mapa = {
            TurnoChoices.A: time(7, 0),
            TurnoChoices.B: time(16, 48),
            TurnoChoices.HC: time(8, 0),
        }

        if turno == TurnoChoices.OUTROS:
            return entrada_personalizada

        return mapa.get(turno)

    @staticmethod
    def horario_fim(turno, saida_personalizada):
        mapa = {
            TurnoChoices.A: time(16, 48),
            TurnoChoices.B: time(2, 0),
            TurnoChoices.HC: time(17, 48),
        }

        if turno == TurnoChoices.OUTROS:
            return saida_personalizada

        return mapa.get(turno)

    @staticmethod
    def turno_noturno(turno):
        return turno == TurnoChoices.B
