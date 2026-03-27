from django.http import JsonResponse

from ..queries.centro_custo_queries import get_subcentros



def get_subcentros_ajax(request):
    pai_id = request.GET.get("pai_id")
    filhos = get_subcentros(pai_id)
    data = [{"id": f.pk, "descricao": f.descricao} for f in filhos]

    return JsonResponse(data, safe=False)
