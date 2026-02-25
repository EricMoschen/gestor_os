from collections import defaultdict
from decimal import Decimal
from datetime import datetime, time
from django.utils.dateparse import parse_date
from abertura_os.models import AberturaOS
from lancamento_horas.models import ApontamentoHoras

from .horario import calcular_horas, formatar_horas, aplicar_filtro_datas


def processar_relatorio(apontamentos):
    funcoes = defaultdict(lambda: {
        "matricula": "",
        "nome":"",
        "funcao": "Sem função",
        "valor_hora": Decimal("0.00"),
        "normais": Decimal("0"),
        "extra50": Decimal("0"),
        "extra100": Decimal("0"),
    })

    for ap in apontamentos:
        if not ap.data_inicio or not ap.data_fim:
            continue

        normais, extra50, extra100 = ap.calcular_horas()

        normais = Decimal(normais)
        extra50 = Decimal(extra50)
        extra100 = Decimal(extra100)

        funcao_obj = getattr(ap.colaborador, "funcao", None)
        chave_funcao = getattr(funcao_obj, "id", None) or f"sem_funcao_{ap.colaborador.id}"

        item = funcoes[chave_funcao]
        item["matricula"] = ap.colaborador.matricula
        item["nome"] = ap.colaborador.nome
        item["funcao"] = getattr(funcao_obj, "descricao", None) or "Sem Função"

        valor_hora = getattr(funcao_obj, "valor_hora", None)
        item["valor_hora"] = Decimal(valor_hora) if valor_hora else Decimal("0.00")

        item["normais"] += normais
        item["extra50"] += extra50
        item["extra100"] += extra100

    relatorio = []
    totais = {
        "normais": Decimal("0"),
        "extra50": Decimal("0"),
        "extra100": Decimal("0"),
        "geral_horas": Decimal("0"),
        "geral_valor": Decimal("0.00"),
    }

    for c in funcoes.values():
        total_horas = c["normais"] + c["extra50"] + c["extra100"]

        # 🔥 Cálculo financeiro
        valor_normais = c["valor_hora"] * c["normais"]
        valor_50 = c["valor_hora"] * Decimal("1.5") * c["extra50"]
        valor_100 = c["valor_hora"] * Decimal("2.0") * c["extra100"]
        total_valor = valor_normais + valor_50 + valor_100

        # Totais gerais
        totais["normais"] += c["normais"]
        totais["extra50"] += c["extra50"]
        totais["extra100"] += c["extra100"]
        totais["geral_horas"] += total_horas
        totais["geral_valor"] += total_valor

        relatorio.append({
            "funcao": c["funcao"],
            "matricula": c["matricula"],
            "nome": c["nome"],

            "valor_hora_fmt": f"R$ {c['valor_hora']:.2f}",

            "horas_normais_fmt": formatar_horas(c["normais"]),
            "horas_50_fmt": formatar_horas(c["extra50"]),
            "horas_100_fmt": formatar_horas(c["extra100"]),
            "total_fmt": formatar_horas(total_horas),

            # 🔥 valores calculados
            "valor_normais_fmt": f"R$ {valor_normais:.2f}",
            "valor_50_fmt": f"R$ {valor_50:.2f}",
            "valor_100_fmt": f"R$ {valor_100:.2f}",
            "total_valor_fmt": f"R$ {total_valor:.2f}",
        })

    totais_formatados = {
        "normais": formatar_horas(totais["normais"]),
        "extra50": formatar_horas(totais["extra50"]),
        "extra100": formatar_horas(totais["extra100"]),
        "geral_horas": formatar_horas(totais["geral_horas"]),
        "geral_valor": f"R$ {totais['geral_valor']:.2f}",
    }

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
    apontamentos = (
        ApontamentoHoras.objects
        .select_related("colaborador")
        .filter(ordem_servico=os_obj)
        .order_by("colaborador__matricula", "data_inicio")
    )

    if data_inicio:
        apontamentos = apontamentos.filter(
            data_fim__gte=datetime.combine(data_inicio, time.min)
        )

    if data_fim:
        apontamentos = apontamentos.filter(
            data_inicio__lte=datetime.combine(data_fim, time.max)
        )

    dados = []
    total_segundos = 0

    for ap in apontamentos:
        inicio = ap.data_inicio
        fim = ap.data_fim

        if inicio and fim:
            duracao = fim - inicio
            segundos = int(duracao.total_seconds())
            total_segundos += segundos

            horas = segundos // 3600
            minutos = (segundos % 3600) // 60

            dados.append({
                "matricula": ap.colaborador.matricula,
                "colaborador": ap.colaborador.nome,
                "data": inicio.strftime("%d/%m/%Y"),
                "hora_inicio": inicio.strftime("%H:%M"),
                "hora_fim": fim.strftime("%H:%M"),
                "duracao": f"{horas:02d}:{minutos:02d}",
            })

    total_horas = total_segundos // 3600
    total_minutos = (total_segundos % 3600) // 60

    total_formatado = f"{int(total_horas):02d}:{int(total_minutos):02d}"

    return dados, total_formatado