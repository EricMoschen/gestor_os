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





# ======================================================================
# Cadastro de Colaboradores
# ======================================================================
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








class AberturaOS(models.Model):

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="ordens_servico",
        null=True,
        blank=True
    )
