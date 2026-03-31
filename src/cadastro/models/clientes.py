from django.db import models


class Cliente(models.Model):

    codigo = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        verbose_name="Código do Cliente"
    )

    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do Cliente"
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


