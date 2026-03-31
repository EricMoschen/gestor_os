from django.db import models


class Funcao_colab(models.Model):
    
    descricao =  models.CharField(
        max_length=255,
        unique = True,
        verbose_name= 'Descricao da Função'
        )
    
    valor_hora = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00,
        verbose_name='Valor_Hora'
    )
    
    def __str__(self):
        return self.descricao
