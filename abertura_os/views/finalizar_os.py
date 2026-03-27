from django.db import transaction
from django.shortcuts import redirect, render

from ..forms import FinalizacaoOSForm, PecaAplicadaFormSet
from ..models import AberturaOS


def _montar_contexto(ordens, erro=None, finalizacao_form=None, pecas_formset=None):
    return {
        "ordens": ordens,
        "erro": erro,
        "finalizacao_form": finalizacao_form or FinalizacaoOSForm(prefix="finalizacao"),
        "pecas_formset": pecas_formset or PecaAplicadaFormSet(prefix="pecas"),
    }


def finalizar_os_view(request):
    ordens = AberturaOS.objects.all().order_by("numero_os")

    if request.method != "POST":
        return render(request, "finalizar_os/finalizar_os.html", _montar_contexto(ordens))

    numero_os = request.POST.get("numero_os_hidden", "").strip()

    if not numero_os:
        contexto = _montar_contexto(ordens, erro="Número da OS não foi informado.")
        return render(request, "finalizar_os/finalizar_os.html", contexto)

    try:
        ordem = AberturaOS.objects.get(numero_os=numero_os)
    except AberturaOS.DoesNotExist:
        contexto = _montar_contexto(ordens, erro=f"Nenhuma OS encontrada com o número {numero_os}.")
        return render(request, "finalizar_os/finalizar_os.html", contexto)

    if ordem.situacao == AberturaOS.Status.FINALIZADA:
        contexto = _montar_contexto(ordens, erro=f"A OS {numero_os} já está finalizada.")
        return render(request, "finalizar_os/finalizar_os.html", contexto)

    finalizacao_form = FinalizacaoOSForm(request.POST, prefix="finalizacao")
    pecas_formset = PecaAplicadaFormSet(request.POST, prefix="pecas")

    if not (finalizacao_form.is_valid() and pecas_formset.is_valid()):
        contexto = _montar_contexto(
            ordens,
            finalizacao_form=finalizacao_form,
            pecas_formset=pecas_formset,
        )
        return render(request, "finalizar_os/finalizar_os.html", contexto)

    with transaction.atomic():
        finalizacao = finalizacao_form.save(commit=False)
        finalizacao.ordem_servico = ordem
        finalizacao.save()

        pecas_formset.instance = finalizacao
        pecas_formset.save()

        ordem.observacoes = finalizacao.observacoes
        ordem.situacao = AberturaOS.Status.FINALIZADA
        ordem.save(update_fields=["observacoes", "situacao"])

    return redirect("finalizar_os")
