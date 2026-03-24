from relatorios.models import SequenciaOrcamento

def ler_numero_orcamento():
    """Lê número sem incrementar."""
    sequencia = SequenciaOrcamento.objects.filter(chave = "orcamento_global").first()
    return sequencia.ultimo_numero if sequencia else 0

def gerar_proximo_orcamento():
    """Retorna e persiste o próximo número do orçamento em banco de dados"""
    return SequenciaOrcamento.proximo_numero()

