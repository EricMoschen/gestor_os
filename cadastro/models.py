# ======================================================================
# Importações
# ======================================================================
from django.db import models


# ======================================================================
# Cadastro dos Centros de Custos
# ======================================================================
class CentroCusto(models.Model):

    cod_centro = models.PositiveIntegerField(primary_key=True)

    descricao = models.CharField(max_length=100)

    centro_pai = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="subcentros"
    )

    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["descricao"]
        verbose_name = "Centro de Custo"
        verbose_name_plural = "Centros de Custo"

    def __str__(self):
        return self.descricao


