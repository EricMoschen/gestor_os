from django.db import models
from django.utils import timezone
from datetime import datetime, time, timedelta
from src.cadastro.models import Colaborador
from src.abertura_os.models import AberturaOS
from src.lancamento_horas.utils.feriados import eh_feriado_ou_domingo, eh_sabado



class ApontamentoHoras(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.PROTECT,related_name="apontamentos_lancamento")
    ordem_servico = models.ForeignKey(AberturaOS, on_delete=models.PROTECT)

    data_inicio = models.DateTimeField(default=timezone.now)
    data_fim = models.DateTimeField(blank=True, null=True)
    tipo_dia = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.colaborador.nome} - {self.ordem_servico.numero_os}"

    # =====================================================
    # CALCULA HORAS NORMAIS VS EXTRA
    # =====================================================
    def calcular_horas(self):
        from ..services.apontamento_horas_service import ApontamentoHorasService
        return ApontamentoHorasService.calcular_horas(self)

    # =====================================================
    # MÉTODO PARA ENCERRAR APONTAMENTO ABERTO
    # =====================================================
    @classmethod
    def encerrar_aberto(cls, colaborador, referencia_agora=None):
        from ..services.apontamento_horas_service import ApontamentoHorasService
        return ApontamentoHorasService.encerrar_aberto(cls, colaborador, referencia_agora=referencia_agora)
