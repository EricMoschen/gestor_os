## Tabelas Dimenção

- *`Abertura de Ordens De Serviço`* (8/Dia)
-> Campos da Tabela:
    -> Numero
    -> Descrição
    -> Centro Custo (Associa da tabela de cadastro de ativos)
    -> Clientes (Associa a tabelas de clientes)
    -> Motivo da intervenção (Associa a tabela de cadastro de intervenção)
    -> SSM (Sistema de Solicitação de Manutenção)
    -> Situação
    -> Data_abertura


- *`Finalizar  Ordens De Serviço`* (8/Dia)
-> Campos da Tabela:
    -> Os (Associa da tabela de abertura de ordens de serviço)
    -> Descrição Técnica da Avaria
    -> Descrição da Intervenção
    -> Peças Aplicadas
        -> Quantidade 
        -> Descrição
    -> Descrição do Sintoma
    -> Causa
    -> Data com Hora de Inicio 
    -> Data com Hora de Fim
    -> Observações 
    


- *`Cadastro de Ativos`*(10/Ano)
-> Campos da Tabela:
    -> Tag_Pai_ID
    -> Tag
    -> Cod_Centro
    -> Descrição
    -> Ativo


- *`Cadastro de Clientes`* (1/Mês)
-> Campos da Tabela:
    -> ID
    -> Código
    -> Nome
    -> Criado_em
    -> Atualizado_em
    -> Ativo


- *`Cadastro de Colaboradores`* (2/Ano)
-> Campos da Tabela:
    -> ID
    -> Mátricula
    -> Nome
    -> ativo
    -> Função (Associa da Tabela de Função)
    -> Turno (Associa da Tabela Turno com Choices)


- *`Cadastro de Função`* (5/Ano)
-> Campos da Tabela:
    -> ID
    -> Descrição
    -> Valor_hora


- *`Cadastro de Intervenção`* (5/Ano)
-> Campos da Tabela:
    -> Id
    -> Código
    -> Descrição


---

## Tabelas Fato

- *`Apontamento de horas`* (200/Dia)
-> Campos da Tabela:
    -> Colaborador (Associa a tabela de cadastro de colaborador)
    -> Ordem de Serviço (Associa a tabela de abertura de ordem de serviço)
    -> Data Inicio
    -> Data Fim
    -> Tipo do Dia

