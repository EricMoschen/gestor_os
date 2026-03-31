from src.cadastro.models import CentroCusto


def get_centros_pais():
    return CentroCusto.objects.filter(tag_pai__isnull=True).order_by("descricao")


def get_subcentros(pai_id):
    return CentroCusto.objects.filter(tag_pai_id=pai_id).order_by("descricao")
