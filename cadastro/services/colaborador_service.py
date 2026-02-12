from django.db import transaction


def salvar_colaborador(form):
    with transaction.atomic():
        return form.save()


def excluir_colaborador(colaborador):
    with transaction.atomic():
        nome = colaborador.nome
        colaborador.delete()
        return nome
