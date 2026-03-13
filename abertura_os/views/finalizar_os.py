from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from ..models import AberturaOS
from ..utils import finalizar_ordem


def finalizar_os_view(request):
    ordens = AberturaOS.objects.all().order_by("numero_os")
    erro = None

    if request.method == "POST":
        numero_os = request.POST.get("numero_os_hidden", "").strip()
        observacoes = request.POST.get("observacoes", "").strip()

        if not numero_os:
            erro = "Número da OS não foi informado."
        elif not observacoes:
            erro = "Informe a observação antes de finalizar a OS."
        else:
            try:
                ordem = AberturaOS.objects.get(numero_os=numero_os)
                if ordem.situacao == AberturaOS.Status.FINALIZADA:
                    erro = f"A OS {numero_os} já está finalizada."
                    return render(request, "finalizar_os/finalizar_os.html", {
                        "ordens": ordens,
                        "erro": erro
                    })
                
                finalizar_ordem(numero_os, observacoes)
                return redirect("finalizar_os")
            except ObjectDoesNotExist:
                erro = f"Nenhuma OS encontrada com o número {numero_os}."

    return render(request, "finalizar_os/finalizar_os.html", {
        "ordens": ordens,
        "erro": erro
    })
