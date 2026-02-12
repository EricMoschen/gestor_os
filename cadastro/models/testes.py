from django.db import models
from cadastro.models import Colaborador


class ApontamentoHoras(models.Model):
    colaborador = models.ForeignKey(
        Colaborador,
        on_delete=models.CASCADE
    )
