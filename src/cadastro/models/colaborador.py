from django.db import models
from .funcao_colab import Funcao_colab
from src.cadastro.models.choices import TurnoChoices
from src.cadastro.services.horario_service import HorarioService
from src.cadastro.validators.colaborador_validator import validar_horarios_outros


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

    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )


    funcao = models.ForeignKey(
        Funcao_colab,
        on_delete=models.PROTECT,
        related_name="Função_Colaborador",
        null=True,
        blank=True
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
