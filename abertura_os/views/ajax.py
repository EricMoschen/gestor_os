from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from ..queries.centro_custo_queries import get_subcentros



def get_subcentros_ajax(request):

    pai_id = request.GET.get("pai_id")

    filhos = get_subcentros(pai_id)

    data = [
        {
            "id": f.cod_centro,
            "descricao": f.descricao
        }
        for f in filhos
    ]

    return JsonResponse(data, safe=False)
