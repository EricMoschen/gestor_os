# =========================
# HORARIO
# =========================
from .horario import (
    calcular_horas,
    formatar_horas,
    calcular_duracao,
    formatar_duracao,
    aplicar_filtro_datas,
    BR_HOLIDAYS,
)

# =========================
# RELATORIO
# =========================
from .relatorio import (
    processar_relatorio,
    construir_contexto_relatorio_os,
    
)

# =========================
# ORCAMENTO
# =========================
from .orcamento import (
    ler_numero_orcamento,
    gerar_proximo_orcamento,
)
