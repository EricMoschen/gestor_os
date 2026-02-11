def montar_hierarquia(centros):

    def _montar(centro):
        return {
            "centro": centro,
            "filhos": [_montar(filho) for filho in centro.subcentros.all()]
        }

    return [_montar(c) for c in centros]
