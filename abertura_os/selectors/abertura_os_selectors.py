from abertura_os.models import AberturaOS


def listar_os_ativas():
    return (
        AberturaOS.objects
        .filter(situacao=AberturaOS.Status.ABERTA)
        .select_related("cliente", "centro_custo", "motivo_intervencao")
    )


def listar_todas_os():
    return (
        AberturaOS.objects
        .select_related("cliente", "centro_custo", "motivo_intervencao")
        .order_by("-data_abertura")
    )
