from django.db import models
from django.db.models import Q

class CentroCusto(models.Model):

    cod_centro = models.PositiveIntegerField(primary_key=True)

    tenant_id = models.CharField(max_length=36, default="default", db_index=True)

    cod_tag = models.PositiveIntegerField(blank=True, null=True)

    descricao = models.CharField(max_length=100)

    tag_pai = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="subtags"
    )

    cod_do_ativo = models.CharField(max_length=50, blank=True, null=True)

    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["descricao"]
        verbose_name = "Ativo"
        verbose_name_plural = "Ativos"
        constraints = [
            models.UniqueConstraint(
                fields=["tenant_id", "cod_tag"],
                condition=Q(cod_tag__isnull=False),
                name="uniq_cod_tag_por_tenant",
            )
        ]

    def __str__(self):
        return self.descricao

