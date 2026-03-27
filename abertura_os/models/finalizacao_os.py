from django.core.exceptions import ValidationError
from django.db import models


class FinalizacaoOS(models.Model):
    ordem_servico = models.OneToOneField(
        "abertura_os.AberturaOS",
        on_delete=models.CASCADE,
        related_name="finalizacao",
    )
    descricao_tecnica_avaria = models.TextField(
        verbose_name="Descrição Técnica da Avaria"
    )
    descricao_intervencao = models.TextField(
        verbose_name="Descrição da Intervenção"
    )
    descricao_sintoma = models.TextField(
        verbose_name="Descrição do Sintoma"
    )
    causa = models.TextField(verbose_name="Causa")
    data_hora_inicio = models.DateTimeField(verbose_name="Data/Hora de Início")
    data_hora_fim = models.DateTimeField(verbose_name="Data/Hora de Fim")
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações",
    )
    finalizado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-finalizado_em"]
        verbose_name = "Finalização de OS"
        verbose_name_plural = "Finalizações de OS"
        indexes = [
            models.Index(fields=["data_hora_inicio"]),
            models.Index(fields=["data_hora_fim"]),
        ]

    def clean(self):
        super().clean()
        if self.data_hora_fim and self.data_hora_inicio and self.data_hora_fim < self.data_hora_inicio:
            raise ValidationError(
                {"data_hora_fim": "A data/hora de fim deve ser maior ou igual ao início."}
            )

    def __str__(self):
        return f"Finalização {self.ordem_servico.numero_os}"


class PecaAplicada(models.Model):
    finalizacao = models.ForeignKey(
        FinalizacaoOS,
        on_delete=models.CASCADE,
        related_name="pecas_aplicadas",
    )
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade")
    descricao = models.CharField(max_length=255, verbose_name="Descrição")

    class Meta:
        verbose_name = "Peça Aplicada"
        verbose_name_plural = "Peças Aplicadas"
        ordering = ["id"]

    def __str__(self):
        return f"{self.quantidade}x {self.descricao}"