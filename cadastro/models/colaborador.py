from django.db import models
from cadastro.models.choices import TurnoChoices
from cadastro.services.horario_service import HorarioService
from cadastro.validators.colaborador_validator import validar_horarios_outros


class Colaborador(models.Model):

    matricula = models.CharField(
        max_length=4,
        unique=True,
        verbose_name='Matrícula'
    )

    nome = models.CharField(
        max_length=255,
        verbose_name='Nome'
    )

    funcao = models.CharField(
        max_length=150,
        verbose_name='Função'
    )

    valor_hora = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00,
        verbose_name='Valor Hora'
    )

    turno = models.CharField(
        max_length=10,
        choices=TurnoChoices.choices,
        verbose_name='Turno'
    )

    hr_entrada_am = models.TimeField(blank=True, null=True)
    hr_saida_am = models.TimeField(blank=True, null=True)
    hr_entrada_pm = models.TimeField(blank=True, null=True)
    hr_saida_pm = models.TimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"
        ordering = ['nome']

    def __str__(self):
        return f"{self.matricula} - {self.nome}"

    # ===== VALIDAÇÃO =====

    def clean(self):
        validar_horarios_outros(self)

    # ===== REGRAS DE HORÁRIO =====

    def horario_inicio_turno(self):
        return HorarioService.horario_inicio(
            self.turno,
            self.hr_entrada_am
        )

    def horario_fim_turno(self):
        return HorarioService.horario_fim(
            self.turno,
            self.hr_saida_pm
        )

    @property
    def turno_noturno(self):
        return HorarioService.turno_noturno(self.turno)
