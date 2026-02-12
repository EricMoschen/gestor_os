from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from abertura_os.models import AberturaOS


def imprimir_os(request, pk):
    os = get_object_or_404(AberturaOS, pk=pk)
    return render(request, 'imprimir_os/imprimir_os.html', {'os': os})
