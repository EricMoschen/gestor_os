from django.db import models, transaction

class SequenciaOrcamento(models.Model):
    """Controle Transacional de Sequência numérica para o orçamento"""
    chave = models.CharField(max_length=50, unique=True, default="orcamento_global")
    ultimo_numero = models.PositiveIntegerField(default=0)
    atualizado_em =  models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name="Sequência de oramento"
        verbose_name_plural="Sequências de orçamento"

    def __str__(self):
        return f"{self.chave}: {self.ultimo_numero}"
    
    @classmethod
    def proximo_numero(cls,chave:str = "orcamento-global") -> int:
        """Retorna o próximo número da sequência de forma segura para concorrência."""
        with transaction.atomic():
            sequencia, _ = cls.objects.select_for_update().get_or_create(chave=chave)
            sequencia.ultimo_numero += 1
            sequencia.save(update_fields=["ultimo_numero", "atualizado_em"])
            return sequencia.ultimo_numero