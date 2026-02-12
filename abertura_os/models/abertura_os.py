from django.db import models, transaction
from django.utils import timezone

from cadastro.models import CentroCusto, Cliente, Intervencao


class AberturaOS(models.Model):

    class Status(models.TextChoices):
        ABERTA = "AB", "Ativa"
        FINALIZADA = "FI", "Finalizada"

    numero_os = models.CharField(
        max_length=8,
        unique=True,
        editable=False,
        verbose_name="Número da OS"
    )

    descricao_os = models.TextField(verbose_name="Descrição")

    centro_custo = models.ForeignKey(
        CentroCusto,
        on_delete=models.PROTECT,
        related_name="ordens_servico"
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="ordens_servico",
        null=True,
        blank=True
    )

    motivo_intervencao = models.ForeignKey(
        Intervencao,
        on_delete=models.PROTECT,
        related_name="ordens_servico"
    )

    ssm = models.CharField(max_length=10)

    situacao = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.ABERTA
    )

    data_abertura = models.DateTimeField(auto_now_add=True)

    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-data_abertura"]
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"
        indexes = [
            models.Index(fields=["numero_os"]),
            models.Index(fields=["situacao"]),
        ]

    # =====================================================
    # Numeração OS
    # =====================================================
    @classmethod
    def gerar_proximo_numero_os(cls):

        ano = timezone.now().year % 100

        ultima_os = (
            cls.objects
            .filter(numero_os__endswith=f"-{ano}")
            .order_by("-numero_os")
            .first()
        )

        if ultima_os:
            sequencial = int(ultima_os.numero_os.split("-")[0]) + 1
        else:
            sequencial = 1

        return f"{sequencial:03d}-{ano}"

    def save(self, *args, **kwargs):

        if not self.numero_os:
            with transaction.atomic():
                self.numero_os = self.gerar_proximo_numero_os()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"OS {self.numero_os}"
