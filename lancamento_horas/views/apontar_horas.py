from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from ..models.apontamento_horas import ApontamentoHoras
from ..services.apontamento_horas_service import ApontamentoHorasService
from cadastro.models import Colaborador
from abertura_os.models import AberturaOS
import holidays

BR_HOLIDAYS = holidays.Brazil()  # Para verificar feriados



def apontar_horas(request):
    if request.method == "POST":
        matricula = request.POST.get("matricula", "").strip().upper()
        numero_os = request.POST.get("numero_os")
        acao = request.POST.get("acao")

        colaborador = get_object_or_404(
            Colaborador.objects.only(
                "id", "turno", "hr_entrada_am", "hr_saida_am",
                "hr_entrada_pm", "hr_saida_pm", "matricula", "nome"
            ),
            matricula__iexact=matricula
        )

        os_obj = get_object_or_404(
            AberturaOS.objects.only("id", "numero_os", "situacao"),
            numero_os=numero_os
        )

        agora = timezone.now()

        if acao == "iniciar":
            # Bloqueio OS finalizada
            if os_obj.situacao == AberturaOS.Status.FINALIZADA:
                messages.error(
                    request,
                    f"A OS {os_obj.numero_os} está {os_obj.get_situacao_display()} e não permite apontamentos."
                )
                return redirect("lancamento_horas:apontar_horas")

            aberto = ApontamentoHoras.objects.filter(
                colaborador=colaborador,
                data_fim__isnull=True
            ).order_by("-data_inicio").first()

            if aberto:
                try:
                    ApontamentoHoras.encerrar_aberto(colaborador)
                except ValueError as e:
                    messages.error(
                        request,
                        f"Erro! OS {aberto.ordem_servico.numero_os} em aberto. {e}"
                    )
                    return redirect("lancamento_horas:apontar_horas")

            tipo_dia = ApontamentoHorasService.classificar_tipo_dia(agora.date())

            ApontamentoHoras.objects.create(
                colaborador=colaborador,
                ordem_servico=os_obj,
                data_inicio=agora,
                tipo_dia=tipo_dia
            )
            messages.success(request, f"Início da OS {os_obj.numero_os} registrado.")

        elif acao == "finalizar":
            aberto = ApontamentoHoras.objects.filter(
                colaborador=colaborador,
                data_fim__isnull=True
            ).order_by("-data_inicio").first()

            if not aberto:
                messages.warning(request, "Nenhuma OS em andamento para este colaborador.")
                return redirect("lancamento_horas:apontar_horas")

            if aberto.data_inicio > agora:
                messages.error(request, "Erro! Horário de início maior que horário de fim.")
                return redirect("lancamento_horas:apontar_horas")

            aberto.data_fim = agora
            aberto.save(update_fields=["data_fim"])
            messages.success(request, f"OS {aberto.ordem_servico.numero_os} finalizada.")

        return redirect("lancamento_horas:apontar_horas")

    # GET → listar ordens de serviço
    ordens = AberturaOS.objects.select_related("centro_custo", "cliente").only(
        "numero_os", "descricao_os", "situacao","data_abertura", "centro_custo__descricao", "cliente__nome"
    ).order_by("-data_abertura")

    return render(request, "apontamento_horas/apontamento_horas.html", {"ordens": ordens})
