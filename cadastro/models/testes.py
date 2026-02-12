from django.db import models
from cadastro.models import Colaborador, Intervencao, Cliente


class ApontamentoHoras(models.Model):
    colaborador = models.ForeignKey(
        Colaborador,
        on_delete=models.CASCADE
    )
    intervencao = models.ForeignKey(
        Intervencao,
        on_delete=models.PROTECT,
        related_name="aberturas"
    )
    cliente = models.ForeignKey(
    Cliente,
    on_delete=models.PROTECT,
    related_name="ordens_servic"
)
