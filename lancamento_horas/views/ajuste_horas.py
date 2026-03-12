from datetime import date, datetime, timedelta

from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from abertura_os.models import AberturaOS
from cadastro.models import Colaborador
from lancamento_horas.services.apontamento_horas_service import ApontamentoHorasService

from ..models.apontamento_horas import ApontamentoHoras


def _parse_datetime_local(value):    
    datahora = datetime.fromisoformat(value)

    if not settings.USE_TZ:
        return datahora
    
    if timezone.is_naive(datahora):
        return timezone.make_aware(datahora)
    
    return datahora

def _ajustar_fim_virada_dia(inicio: datetime, fim: datetime):
    """Quando o Fim é menor ou igual ao inicio, considera virada de dia."""
    if fim <= inicio:
        return fim + timedelta(days=1), True
    return fim, False

def _intervalo_competencia(competencia: str | None):
    hoje = timezone.localdate()
    competencia_valida = competencia or hoje.strftime("%Y-%m")

    try:
        ano, mes = map(int, competencia_valida.split("-"))
        data_referencia = date(ano, mes, 1)
    except(ValueError,TypeError):
        data_referencia = date(hoje.year, hoje.month, 1)

    if data_referencia.month == 1:
        ano_anterior, mes_anterior = data_referencia.year - 1, 12
    else:
        ano_anterior, mes_anterior = data_referencia.year, data_referencia.month - 1

    data_inicio = date(ano_anterior, mes_anterior, 21)
    data_fim = date(data_referencia.year, data_referencia.month, 20)

    return data_referencia.strftime("%Y-%m"), data_inicio, data_fim


def _gerar_competencias(apontamentos):
    meses_pt = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", 
        "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    primeira_data = apontamentos.order_by("data_inicio").values_list("data_inicio", flat=True).first()
    ultima_data = apontamentos.order_by("-data_inicio").values_list("data_inicio", flat=True).first()

    if not primeira_data or not ultima_data:
        hoje = timezone.localdate()
        chave = hoje.strftime("%Y-%m")
        return [{"valor":chave, "label": f"{meses_pt[hoje.month - 1]}/{hoje.year}"}]
    
    cursor = date(primeira_data.year, primeira_data.month, 1)
    limite = date(ultima_data.year, ultima_data.month, 1)
    competencia = []

    while cursor<= limite:
        competencia.append(
            {
                "valor": cursor.strftime("%Y-%m"),
                "label": f"{meses_pt[cursor.month - 1]}/{cursor.year}",

            }
        )

        if cursor.month == 12:
            cursor =  date(cursor.year + 1, 1, 1)
        else:
            cursor = date(cursor.year, cursor.month + 1, 1)

    return list(reversed(competencia))



def ajuste_horas(request):
    if request.method == "POST":

        acao = request.POST.get("acao", "ajustar")

        if acao == "criar":
            matricula = request.POST.get("matricula", "").strip().upper()
            numero_os = request.POST.get("numero_os", "").strip().upper()
            data_raw= request.POST.get("data", "").strip()
            hora_inicio_raw = request.POST.get("hora_inicio", "").strip()
            hora_fim_raw = request.POST.get("hora_fim", "").strip()

            if not (matricula and numero_os and data_raw and hora_inicio_raw and hora_fim_raw):
                messages.error(request, "Preencha todos os campos para cadastrar uma nova ocorrência.")
                return redirect("lancamento_horas:ajuste_horas")
            
            colaborador = Colaborador.objects.filter(matricula__iexact=matricula).first()
            if not colaborador:
                messages.error(request, "Matrícula não encontrada.")
                return redirect("lancamento_horas:ajuste_horas")

            os_obj = AberturaOS.objects.filter(numero_os__iexact=numero_os).first()
            if not os_obj:
                messages.error(request, "Número da OS não encontrado.")
                return redirect("lancamento_horas:ajuste_horas")

            try:
                inicio = _parse_datetime_local(f"{data_raw}T{hora_inicio_raw}")
                fim = _parse_datetime_local(f"{data_raw}T{hora_fim_raw}")
            except ValueError:
                messages.error(request, "Data ou horário inválido.")
                return redirect("lancamento_horas:ajuste_horas")
            

            fim, virou_dia = _ajustar_fim_virada_dia(inicio, fim)
            
            ApontamentoHoras.objects.create(
                colaborador=colaborador,
                ordem_servico=os_obj,
                data_inicio=inicio,
                data_fim=fim,
                tipo_dia=ApontamentoHorasService.classificar_tipo_dia(inicio.date()),
            )

            if virou_dia:
                messages.warning(
                    request,
                    "Horário Ajustado para virada de dia (término no dia seguinte)"
                )

            messages.success(request, f"Nova ocorrência da OS {os_obj.numero_os} cadastrada com sucesso.")
            return redirect("lancamento_horas:ajuste_horas")

        apontamento = get_object_or_404(ApontamentoHoras, pk=request.POST.get("apontamento_id"))

        inicio_raw = request.POST.get("data_inicio", "").strip()
        fim_raw = request.POST.get("data_fim", "").strip()

        if not inicio_raw:
            messages.error(request, "Preencha a data/hora de início.")
            return redirect("lancamento_horas:ajuste_horas")

        try:
            inicio = _parse_datetime_local(inicio_raw)
        except ValueError:
            messages.error(request, "Data de início inválida.")
            return redirect("lancamento_horas:ajuste_horas")

        fim = None
        if fim_raw:
            try:
                fim = _parse_datetime_local(fim_raw)
            except ValueError:
                messages.error(request, "Data de fim inválida.")
                return redirect("lancamento_horas:ajuste_horas")
            if fim <= inicio:
                messages.error(request, "Horário de fim deve ser maior que início.")
                return redirect("lancamento_horas:ajuste_horas")

        apontamento.data_inicio = inicio
        apontamento.data_fim = fim
        apontamento.tipo_dia = ApontamentoHorasService.classificar_tipo_dia(inicio.date())
        apontamento.save(update_fields=["data_inicio", "data_fim", "tipo_dia"])

        messages.success(request, f"Apontamento da OS {apontamento.ordem_servico.numero_os} atualizado.")
        return redirect("lancamento_horas:ajuste_horas")

    competencia_raw =  request.GET.get("competencia")
    competencia_selecionada, periodo_inicio, periodo_fim =  _intervalo_competencia(competencia_raw)

    apontamentos_base = ApontamentoHoras.objects.select_related("colaborador", "ordem_servico")
    competencia = _gerar_competencias(apontamentos_base)
    apontamentos = apontamentos_base.filter(
        data_inicio__date__gte=periodo_inicio,
        data_inicio__date__lte=periodo_fim,
    ).order_by("-data_inicio")

    context = {
        "apontamentos": apontamentos,
        "competencias": competencia,
        "competencia_selecionada": competencia_selecionada,
        "periodo_inicio": periodo_inicio,
        "periodo_fim": periodo_fim,
        "kpis": {
            "total": apontamentos.count(),
            "em_aberto": apontamentos.filter(data_fim__isnull=True).count(),
            "encerrados": apontamentos.filter(data_fim__isnull=False).count(),
            "colaboradores_ativos": apontamentos.filter(data_fim__isnull=True).values("colaborador_id").distinct().count()
        }
    }
    return render(request, "ajuste_horas/ajuste_horas.html", context)
