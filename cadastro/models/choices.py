from django.db import models


class TurnoChoices(models.TextChoices):
    A = 'A', 'A - 07:00 às 11:00 / 12:00 às 16:48'
    B = 'B', 'B - 16:48 às 19:00 / 20:00 às 02:00'
    HC = 'HC', 'H/C - 08:00 às 12:00 / 13:00 às 17:48'
    OUTROS = 'OUTROS', 'Outros'
