from collections import defaultdict
from datetime import datetime, time
from django.utils.dateparse import parse_date
from abertura_os.models import AberturaOS
from lancamento_horas.models import ApontamentoHoras

from .horario import calcular_horas, formatar_horas, aplicar_filtro_datas


def processar_relatorio(apontamentos):
    colaboradores = defaultdict(lambda: {
        "matricula": "",
        "nome": "",
        "valor_hora":None,
        "normais": 0,
        "extra50": 0,
        "extra100": 0,
    })

    for ap in apontamentos:
        if not ap.data_inicio or not ap.data_fim:
            continue
        normais, extra50, extra100 = calcular_horas(ap.data_inicio, ap.data_fim, ap.colaborador)
        col = colaboradores[ap.colaborador.id]
        col["matricula"] = ap.colaborador.matricula
        col["nome"] = ap.colaborador.nome
        col["valor_hora"] = getattr(getattr(ap.colaborador,"funcao", None),"valor_hora", None)
        col["normais"] += normais
        col["extra50"] += extra50
        col["extra100"] += extra100

    relatorio = []
    totais = {"normais": 0, "extra50": 0, "extra100": 0, "geral": 0}

    for c in colaboradores.values():
        total = c["normais"] + c["extra50"] + c["extra100"]
        totais["normais"] += c["normais"]
        totais["extra50"] += c["extra50"]
        totais["extra100"] += c["extra100"]
        totais["geral"] += total

        relatorio.append({
            "matricula": c["matricula"],
            "nome": c["nome"],
            "valor_hora_fmt": f"R$ {c['valor_hora']:.2f}" if c["valor_hora"] is not None else "--",
            "horas_normais_fmt": formatar_horas(c["normais"]),
            "horas_50_fmt": formatar_horas(c["extra50"]),
            "horas_100_fmt": formatar_horas(c["extra100"]),
            "total_fmt": formatar_horas(total),
        })

    totais_formatados = {k: formatar_horas(v) for k, v in totais.items()}
    return relatorio, totais_formatados


def construir_contexto_relatorio_os(request):
    numero_os = request.GET.get("os")
    data_inicio = parse_date(request.GET.get("data_inicio") or "")
    data_fim = parse_date(request.GET.get("data_fim") or "")

    ordem_servico = None
    relatorio = []
    totais = None

    apontamentos = ApontamentoHoras.objects.select_related("colaborador", "ordem_servico")

    if numero_os:
        ordem_servico = AberturaOS.objects.get(numero_os=numero_os)
        apontamentos = apontamentos.filter(ordem_servico=ordem_servico)

    if data_inicio:
        apontamentos = apontamentos.filter(data_fim__gte=datetime.combine(data_inicio, time.min))
    if data_fim:
        apontamentos = apontamentos.filter(data_inicio__lte=datetime.combine(data_fim, time.max))

    if apontamentos.exists():
        relatorio, totais = processar_relatorio(apontamentos)

    return {
        "os_detalhes": ordem_servico,
        "relatorio": relatorio,
        "totais": totais,
        "filtro_os": numero_os,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }


def montar_dados_log_os(os_obj, data_inicio=None, data_fim=None):
    apontamentos = ApontamentoHoras.objects.filter(ordem_servico=os_obj)
    if data_inicio:
        apontamentos = apontamentos.filter(data_inicio__gte=data_inicio)
    if data_fim:
        apontamentos = apontamentos.filter(data_fim__lte=data_fim)

    dados = []
    total_segundos = 0

    for ap in apontamentos:
        inicio = ap.data_inicio
        fim = ap.data_fim
        if fim and inicio:
            duracao = fim - inicio
            total_segundos += duracao.total_seconds()
            horas = duracao.seconds // 3600
            minutos = (duracao.seconds % 3600) // 60
            dados.append({
                "colaborador": ap.colaborador.nome,
                "inicio": inicio.strftime("%d/%m/%Y %H:%M"),
                "fim": fim.strftime("%d/%m/%Y %H:%M"),
                "duracao": f"{horas:02d}:{minutos:02d}"
            })

    total_horas = int(total_segundos // 3600)
    total_minutos = int((total_segundos % 3600) // 60)
    return dados, f"{total_horas:02d}:{total_minutos:02d}"
