from datetime import datetime

from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from abertura_os.models import AberturaOS
from cadastro.models import Colaborador
from lancamento_horas.services.apontamento_horas_service import ApontamentoHorasService

from ..models.apontamento_horas import ApontamentoHoras


def __parse_datetime_loca(value):    
    datahora = datetime.fromisoformat(value)

    if not settings.USE_TZ:
        return datahora
    
    if timezone.is_naive(datahora):
        return timezone.make_aware(datahora)
    
    return datahora

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
                inicio = __parse_datetime_loca(f"{data_raw}T{hora_inicio_raw}")
                fim = __parse_datetime_loca(f"{data_raw}T{hora_fim_raw}")
            except ValueError:
                messages.error(request, "Data ou horário inválido.")
                return redirect("lancamento_horas:ajuste_horas")
            

            if fim <= inicio:
                messages.error(request, "Horário de fim deve ser maior que início.")
                return redirect("lancamento_horas:ajuste_horas")
            
            ApontamentoHoras.objects.create(
                colaborador=colaborador,
                ordem_servico=os_obj,
                data_inicio=inicio,
                data_fim=fim,
                tipo_dia=ApontamentoHorasService.classificar_tipo_dia(inicio.date()),
            )

            messages.success(request, "Nova ocorrência da OS {os_obj.numero_os} cadastrada com sucesso.")
            return redirect("lancamento_horas:ajuste_horas")

        apontamento = get_object_or_404(ApontamentoHoras, pk=request.POST.get("apontamento_id"))

        inicio_raw = request.POST.get("data_inicio", "").strip()
        fim_raw = request.POST.get("data_fim", "").strip()

        if not inicio_raw:
            messages.error(request, "Preencha a data/hora de início.")
            return redirect("lancamento_horas:ajuste_horas")

        try:
            inicio = __parse_datetime_loca(inicio_raw)
        except ValueError:
            messages.error(request, "Data de início inválida.")
            return redirect("lancamento_horas:ajuste_horas")

        fim = None
        if fim_raw:
            try:
                fim = __parse_datetime_loca(fim_raw)
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

    apontamentos = ApontamentoHoras.objects.select_related("colaborador", "ordem_servico").order_by("-data_inicio")
    context = {
        "apontamentos": apontamentos,
        "kpis": {
            "total": apontamentos.count(),
            "em_aberto": apontamentos.filter(data_fim__isnull=True).count(),
            "encerrados": apontamentos.filter(data_fim__isnull=False).count(),
            "colaboradores_ativos": apontamentos.filter(data_fim__isnull=True).values("colaborador_id").distinct().count()
        }
    }
    return render(request, "ajuste_horas/ajuste_horas.html", context)
