from django.shortcuts import get_object_or_404
from ..models import AberturaOS

def finalizar_ordem(numero_os: str, observacoes: str):
    """
    Finaliza a OS atualizando observações e situação para 'FI'.
    Lança Http404 se não encontrar a OS.
    """
    numero_os = numero_os.strip()
    os_obj = get_object_or_404(AberturaOS, numero_os=numero_os)
    os_obj.observacoes = observacoes.strip()
    os_obj.situacao = "FI"
    os_obj.save()
    return os_obj
