from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from ..models.apontamento_horas import ApontamentoHoras




def ajuste_horas_supervisor(request):
    if request.method == "POST":
        apontamento = get_object_or_404(ApontamentoHoras, pk=request.POST.get("apontamento_id"))

        inicio_raw = request.POST.get("data_inicio", "").strip()
        fim_raw = request.POST.get("data_fim", "").strip()

        if not inicio_raw:
            messages.error(request, "Preencha a data/hora de início.")
            return redirect("ajuste_horas_supervisor")

        try:
            inicio = timezone.make_aware(datetime.fromisoformat(inicio_raw))
        except ValueError:
            messages.error(request, "Data de início inválida.")
            return redirect("ajuste_horas_supervisor")

        fim = None
        if fim_raw:
            try:
                fim = timezone.make_aware(datetime.fromisoformat(fim_raw))
            except ValueError:
                messages.error(request, "Data de fim inválida.")
                return redirect("ajuste_horas_supervisor")
            if fim <= inicio:
                messages.error(request, "Horário de fim deve ser maior que início.")
                return redirect("ajuste_horas_supervisor")

        apontamento.data_inicio = inicio
        apontamento.data_fim = fim
        apontamento.tipo_dia = ApontamentoHoras.classificar_tipo_dia(inicio.date())
        apontamento.save(update_fields=["data_inicio", "data_fim", "tipo_dia"])

        messages.success(request, f"Apontamento da OS {apontamento.ordem_servico.numero_os} atualizado.")
        return redirect("ajuste_horas_supervisor")

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
