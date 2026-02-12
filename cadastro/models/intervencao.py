from django.db import models


class Intervencao(models.Model):
    id = models.BigAutoField(primary_key=True)

    codigo = models.PositiveIntegerField(
        unique=True,
        verbose_name="Código"
    )

    descricao = models.CharField(
        max_length=200,
        verbose_name="Descrição"
    )

    class Meta:
        db_table = "intervencao"
        verbose_name = "Intervenção"
        verbose_name_plural = "Intervenções"
        ordering = ["codigo"]
        indexes = [
            models.Index(fields=["descricao"]),
        ]

    def __str__(self) -> str:
        return f"{self.codigo} - {self.descricao}"

