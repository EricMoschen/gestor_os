from datetime import datetime, timedelta, time
from collections import defaultdict
from django.utils import timezone
import holidays

BR_HOLIDAYS = holidays.Brazil()


def formatar_horas(horas: float) -> str:
    if not horas or horas <= 0:
        return "00:00"
    h = int(horas)
    m = int(round((horas - h) * 60))
    return f"{h:02d}:{m:02d}"


def calcular_duracao(inicio, fim):
    if not fim or not inicio:
        return timedelta()
    return fim - inicio


def formatar_duracao(td: timedelta):
    total_segundos = int(td.total_seconds())
    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60
    return f"{horas}h{minutos:02d}"


def aplicar_filtro_datas(queryset, data_inicio=None, data_fim=None):
    if data_inicio and data_fim:
        return queryset.filter(
            data_inicio__lte=datetime.combine(data_fim, time.max),
            data_fim__gte=datetime.combine(data_inicio, time.min),
        )
    if data_inicio:
        return queryset.filter(data_fim__gte=datetime.combine(data_inicio, time.min))
    if data_fim:
        return queryset.filter(data_inicio__lte=datetime.combine(data_fim, time.max))
    return queryset


def calcular_horas(inicio, fim, colaborador=None):
    """
    Calcula horas normais, 50% e 100%.
    Simplificado: retorna apenas horas normais por enquanto.
    """
    duracao = fim - inicio
    horas = duracao.total_seconds() / 3600
    normais = horas
    h50 = 0
    h100 = 0
    return normais, h50, h100
