# Definição funcional das tabelas — Gestor OS

Esta visão resume as entidades persistidas atualmente pelos models Django.

---

## Tabelas de dimensão / cadastro

### `CentroCusto` — ativos e centros hierárquicos

- `cod_centro`: chave primária numérica.
- `tenant_id`: identificador lógico do tenant, padrão `default`.
- `cod_tag`: código de tag opcional, único por tenant quando preenchido.
- `descricao`: descrição do ativo/centro.
- `tag_pai`: relacionamento opcional com outro `CentroCusto`.
- `cod_do_ativo`: código textual opcional do ativo.
- `ativo`: status de uso.

### `Cliente`

- `codigo`: código único e indexado.
- `nome`: nome do cliente.
- `criado_em`: data/hora de criação.
- `atualizado_em`: data/hora da última alteração.
- `ativo`: status de uso.

### `Intervencao`

- `id`: chave primária.
- `codigo`: código numérico único.
- `descricao`: descrição única da intervenção.

### `Funcao_colab`

- `id`: chave primária padrão Django.
- `descricao`: descrição única da função.
- `valor_hora`: valor-hora usado nos relatórios/orçamentos.

### `Colaborador`

- `id`: chave primária padrão Django.
- `matricula`: matrícula única de até 4 caracteres.
- `nome`: nome do colaborador.
- `ativo`: status de uso.
- `funcao`: FK protegida para `Funcao_colab`.
- `turno`: choice `A`, `B`, `HC` ou `OUTROS`.
- `hr_entrada_am`, `hr_saida_am`, `hr_entrada_pm`, `hr_saida_pm`: horários customizados para turno `OUTROS`.

---

## Tabelas operacionais / fato

### `AberturaOS` — ordens de serviço

- `id`: chave primária padrão Django.
- `numero_os`: número único gerado automaticamente no formato `NNNN-AA`.
- `descricao_os`: descrição da OS.
- `centro_custo`: FK protegida para `CentroCusto`.
- `cliente`: FK protegida opcional para `Cliente`.
- `motivo_intervencao`: FK protegida para `Intervencao`.
- `ssm`: código SSM.
- `situacao`: `AB` para ativa ou `FI` para finalizada.
- `data_abertura`: data/hora automática da abertura.
- `observacoes`: texto opcional.

### `FinalizacaoOS`

- `id`: chave primária padrão Django.
- `ordem_servico`: relacionamento um-para-um com `AberturaOS`.
- `descricao_tecnica_avaria`: descrição técnica da avaria.
- `descricao_intervencao`: descrição da intervenção realizada.
- `descricao_sintoma`: descrição do sintoma.
- `causa`: causa identificada.
- `data_hora_inicio`: início da intervenção/finalização.
- `data_hora_fim`: fim da intervenção/finalização.
- `observacoes`: observações opcionais.
- `finalizado_em`: timestamp automático.

### `PecaAplicada`

- `id`: chave primária padrão Django.
- `finalizacao`: FK para `FinalizacaoOS`.
- `quantidade`: quantidade aplicada.
- `descricao`: descrição da peça.

### `ApontamentoHoras`

- `id`: chave primária padrão Django.
- `colaborador`: FK protegida para `Colaborador`.
- `ordem_servico`: FK protegida para `AberturaOS`.
- `data_inicio`: início do apontamento, com padrão `timezone.now`.
- `data_fim`: fim do apontamento, opcional enquanto aberto.
- `tipo_dia`: classificação textual auxiliar.

### `SequenciaOrcamento`

- `id`: chave primária padrão Django.
- `chave`: identificador único da sequência.
- `ultimo_numero`: último número emitido.
- `atualizado_em`: timestamp automático da última atualização.

---

## Relacionamentos principais

- Uma OS pertence a um centro de custo, pode ter cliente e sempre possui uma intervenção.
- Uma OS pode ter uma finalização; a finalização pode ter várias peças aplicadas.
- Um apontamento pertence a um colaborador e a uma OS.
- Um colaborador pode estar associado a uma função; a função fornece o valor-hora para relatórios.
- Centros de custo podem formar árvore por `tag_pai`.