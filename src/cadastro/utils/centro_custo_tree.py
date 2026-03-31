def montar_hierarquia(centros):

    def _montar(centro):
        return {"centro": centro, "filhos": [_montar(filho) for filho in centro.subtags.all()]}

    return [_montar(c) for c in centros]
