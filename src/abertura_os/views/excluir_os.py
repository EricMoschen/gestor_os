from django.shortcuts import redirect, get_object_or_404

from src.abertura_os.models import AberturaOS


def excluir_os(request, pk):
    os_obj = get_object_or_404(AberturaOS, pk=pk)
    os_obj.delete()
    return redirect("abrir_os")
