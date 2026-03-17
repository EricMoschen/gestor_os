from django.db import transaction


def salvar_colaborador(form):
    with transaction.atomic():
        return form.save()


def alternar_status_colaborador(colaborador):
    with transaction.atomic():
        colaborador.ativo = not colaborador.ativo
        colaborador.save(update_fields=["ativo"])
        return colaborador
