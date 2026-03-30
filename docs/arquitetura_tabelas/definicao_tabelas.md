
[![Abrir definição de tabelas](https://via.placeholder.com/150)](z - arquitetura_tabelas_expicação/definicao_tabelas.md)
---

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


---

## Tabelas Técnicas


- *`relatorios_sequenciaorcamento`* 
-> Campos da Tabela:
    -> id
    -> chave
    -> ultimo_numero
    -> atualizado_em (controle de sequência; técnico/controle transacional)


- *`auth_group`* 
-> Campos da Tabela:
    -> ID
    -> Name

- *`auth_group_permissions`* 
-> Campos da Tabela:
    -> ID
    -> group_id
    -> permission_id


- *`auth_permission`* 
-> Campos da Tabela:
    -> ID
    -> content_type_id
    -> codename
    -> name

- *`auth_user`* 
-> Campos da Tabela:
    -> ID
    -> password
    -> last_login
    -> is_superuser
    -> username
    -> last_name
    -> email
    -> is_staff
    -> is_active
    -> date_joined
    -> first_name


- *`auth_user_groups`* 
-> Campos da Tabela:
    -> ID
    -> user_id
    -> group_id
    

- *`auth_user_user_permissions`* 
-> Campos da Tabela:
    -> ID
    -> user_id
    -> permission_id


- *`django_admin_log`* 
-> Campos da Tabela:
    -> ID
    -> object_id
    -> object_repr
    -> action_flag
    -> change_message
    -> content_type_id
    -> user_id
    -> action_time


- *`django_content_type`* 
-> Campos da Tabela:
    -> ID
    -> app_label
    -> model

    
- *`django_migrations`* 
-> Campos da Tabela:
    -> ID
    -> app
    -> name
    -> applied


- *`django_session`* 
-> Campos da Tabela:
    -> session_key
    -> session_data
    -> expire_date


