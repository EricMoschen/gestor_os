from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from ..models.apontamento_horas import ApontamentoHoras
from ..services.apontamento_horas_service import ApontamentoHorasService
from cadastro.models import Colaborador
from abertura_os.models import AberturaOS

def apontar_horas(request):
    if request.method == "POST":
        matricula = request.POST.get("matricula", "").strip().upper()
        numero_os = request.POST.get("numero_os", "").strip()
        acao = request.POST.get("acao")

        colaborador =  Colaborador.objects.only(
            "id", "turno", "hr_entrada_am", "hr_saida_am",
            "hr_entrada_pm","hr_saida_pm", "matricula", "nome"
        ).filter(matricula__iexact=matricula).first()

        if not colaborador:
            messages.error(request, "Mátricula não encontrada.")
            return redirect("lancamento_horas:apontar_horas")

        agora = timezone.now()

        if acao == "iniciar":
            if not numero_os:
                messages.error(request, "Informe o número da OS para inicia o apontamento.")
                return redirect("lancamento_horas:apontar_horas")
            os_obj =  AberturaOS.objects.only("id", "numero_os","situacao").filter(
                numero_os__iexact=numero_os
            ).first()

            if not os_obj:
                messages.error(request, "Número da OS não encontrado.")
            
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
                except (ValueError, AttributeError) as erro:
                    messages.error(
                        request,
                        f"A OS {aberto.ordem_servico.numero_os} ainda está em andamento para  {aberto.colaborador.nome}: {erro}."
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

            if numero_os and aberto.ordem_servico.numero_os != numero_os:
                messages.error(
                    request,
                    f"A OS em andamento para o colaborador informado é: {aberto.ordem_servico.numero_os}."
                )

                return redirect("lancamento_horas:apontar_horas")
            
            if aberto.data_inicio > agora:
                messages.error(request, "Erro! Horário de início maior que horário de fim.")
                return redirect("lancamento_horas:apontar_horas")

            aberto.data_fim = agora
            aberto.save(update_fields=["data_fim"])
            messages.success(request, f"OS {aberto.ordem_servico.numero_os} finalizada.")

        else:
            messages.error(request, "Ação inválida para apontamento de horas.")
        return redirect("lancamento_horas:apontar_horas")

    # GET → listar ordens de serviço
    ordens = AberturaOS.objects.select_related("centro_custo", "cliente").only(
        "numero_os", "descricao_os", "situacao","data_abertura", "centro_custo__descricao", "cliente__nome"
    ).order_by("-data_abertura")

    return render(request, "apontamento_horas/apontamento_horas.html", {"ordens": ordens})
