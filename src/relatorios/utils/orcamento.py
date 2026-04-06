from src.relatorios.models import SequenciaOrcamento

def ler_numero_orcamento():
    sequencia = SequenciaOrcamento.objects.filter(chave = "orcamento_global").first()
    return sequencia.ultimo_numero if sequencia else 0

def gerar_proximo_orcamento():
    return SequenciaOrcamento.proximo_numero()

