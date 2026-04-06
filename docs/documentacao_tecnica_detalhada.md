# Documentação Técnica Detalhada — Gestor OS
---

## 1. Visão geral de arquitetura

O sistema está organizado em apps Django com separação por domínio:

- `config`: autenticação, autorização, sessão e roteamento raiz.
- `dashboard`: menu inicial com cards por papel.
- `cadastro`: dados mestres (ativos, clientes, intervenções, colaboradores e funções).
- `abertura_os`: ciclo de vida da ordem de serviço (abertura, edição, finalização, impressão).
- `lancamento_horas`: apontamento e ajuste de horas por colaborador/OS.
- `relatorios`: consolidação técnico-financeira, logs e numeração de orçamento.

Padrão dominante:

- **Views** tratam request/response e mensagens de interface.
- **Services** centralizam regras de negócio.
- **Selectors/Queries** encapsulam consultas com anotações e filtros.
- **Models** guardam estrutura, validações e regras de persistência.
- **Utils** implementam algoritmos transversais (PDF, cálculo, períodos etc.).

---

## 2. Módulo `config` (core do projeto)

### 2.1 Controle de acesso por papel (`src/config/access_control.py`)

- `ensure_roles_exist()`
  - Garante que os grupos `ADM`, `PCM`, `Supervisor`, `Almoxarife`, `Fabrica` existam no banco.
  - É chamado no login/dashboard para bootstrap de segurança.
- `user_has_any_role(user, allowed_roles)`
  - Retorna `False` para não autenticados.
  - Retorna `True` para superusuário.
  - Caso contrário, valida pertencimento do usuário a qualquer papel permitido.
- `role_required(allowed_roles)`
  - Decorator de proteção de views.
  - Envolve a view com `login_required` + verificação de grupo.
  - Em negação, injeta `messages.error` e redireciona para `dashboard`.

### 2.2 Autenticação e sessão (`src/config/auth_views.py`)

- `_get_timeout_error_message(timeout_reason)`
  - Traduz o motivo técnico de timeout (`idle` ou `absolute`) em mensagem amigável.
- `login_view(request)`
  - Garante grupos, evita login redundante (usuário já autenticado).
  - Em `POST`, autentica credenciais.
  - Em sucesso, salva na sessão:
    - política de sessão (`session_policy`),
    - timestamp de login,
    - timestamp da última atividade.
- `logout_view(request)`
  - Realiza logout.
  - Se houver timeout explícito, redireciona para login com querystring de motivo.

### 2.3 Política e middleware de timeout (`src/config/session_policy.py` e `src/config/middleware.py`)

- `resolve_session_policy(user)`
  - Usuário no grupo `Fabrica` recebe política especial (`fabrica`).
  - Demais usuários recebem política padrão (`default`).
- `get_session_config(policy)`
  - `default`: timeout por inatividade (10 min) + aviso prévio (2 min).
  - `fabrica`: sem timeout por inatividade e limite absoluto de 8 horas.
- `SessionTimeoutMiddleware.__call__(request)`
  - Ignora usuários anônimos e rotas login/logout.
  - Aplica timeout absoluto por tempo desde login.
  - Aplica timeout por inatividade quando a política usa idle timeout.
  - Atualiza `last_activity_ts` por request autenticada.

### 2.4 Context processor e rotas raiz

- `session_timeout_config(request)` (`src/config/context_processors.py`)
  - Injeta no template os dados da política atual para o frontend mostrar contagem regressiva.
- `urlpatterns` (`src/config/urls.py`)
  - Define login/logout/admin e inclui apps de domínio.

### 2.5 Comando de gestão

- `ensure_superuser.Command.handle()` (`src/config/management/commands/ensure_superuser.py`)
  - Cria superusuário automaticamente quando variáveis de ambiente estão configuradas.

---

## 3. Módulo `dashboard`

### 3.1 View principal (`src/dashboard/views/dashboard_views.py`)

- `dashboard(request)`
  - Define cards agrupados por categorias (OS, Cadastros, Relatórios).
  - Cada card possui lista de papéis permitidos.
  - Filtra dinamicamente os cards visíveis usando `user_has_any_role`.
  - Renderiza `dashboard.html` com apenas as ações autorizadas ao usuário logado.

---

## 4. Módulo `cadastro`

## 4.1 Modelos de dados (`src/cadastro/models/*`)

- `CentroCusto`
  - Estrutura hierárquica por auto-relacionamento (`tag_pai`/`subtags`).
  - Chave primária `cod_centro` (inteiro).
  - Constraint de unicidade condicional por tenant para `cod_tag`.
  - `__str__`: retorna descrição para UX/admin.
- `Cliente`
  - Identificação por `codigo` único.
  - Campo `ativo` para soft lifecycle.
  - `__str__`: `codigo - nome`.
- `Intervencao`
  - Código numérico único + descrição única.
  - `__str__`: `codigo - descrição`.
- `Funcao_colab`
  - Catálogo de função + valor hora.
  - `__str__`: descrição.
- `Colaborador`
  - Matrícula única, nome, turno e horários personalizados para `OUTROS`.
  - `clean()`: delega validação para `validar_horarios_outros`.
  - `horario_inicio_turno()` / `horario_fim_turno()` / `turno_noturno`:
    - encapsulam regra de calendário de trabalho via `HorarioService`.

## 4.2 Forms (`src/cadastro/forms.py`)

- `CentroCustoForm`
  - `__init__`:
    - restringe `tag_pai` para centros raiz,
    - remove o próprio item da lista ao editar,
    - ajusta labels e obrigatoriedade.
  - `clean`:
    - valida `descricao` obrigatória;
    - se for nó filho (`tag_pai` preenchido), exige `cod_tag` e `cod_do_ativo`.
- `IntervencaoForm`
  - ModelForm direto para CRUD simples de intervenção.
- `ColaboradorForm`
  - `__init__(include_status=False)`:
    - remove campo `ativo` quando tela não permite alterar status.
  - `clean`:
    - no turno `OUTROS`, exige quatro horários (entrada/saída manhã e tarde).

## 4.3 Services (`src/cadastro/services/*`)

- `criar_centro_custo(**dados)`
  - Gera `cod_centro` sequencial quando ausente.
  - Define tenant padrão e valida hierarquia circular antes de salvar.
- `atualizar_centro_custo(centro, **dados)`
  - Atualiza campos dinamicamente + validação de hierarquia.
- `_listar_descendentes(centro)`
  - Percorre árvore em largura (BFS) para mapear todos os filhos.
- `excluir_centro_custo(centro, confirmar_exclusao_filhos=False)`
  - Impede exclusão se houver OS vinculadas em qualquer descendente.
  - Exclui descendentes em ordem reversa dentro de transação atômica.
- `salvar_cliente(cliente_id=None, codigo, nome)`
  - Valida unicidade de código e decide create/update.
- `remover_cliente(cliente)`
  - Exclusão direta.
- `salvar_colaborador(form)`
  - Persistência em transação atômica.
- `alternar_status_colaborador(colaborador)`
  - Inverte campo `ativo` de forma transacional.
- `salvar_intervencao(intervencao_id=None, descricao)`
  - Sanitiza descrição, valida vazios, realiza update ou create com código incremental.
- `remover_intervencao(intervencao)`
  - Bloqueia exclusão quando intervenção já é referenciada por OS.
- `HorarioService.horario_inicio(turno, entrada_personalizada)`
- `HorarioService.horario_fim(turno, saida_personalizada)`
- `HorarioService.turno_noturno(turno)`
  - Serviço utilitário para resolver janelas por turno padrão (`A/B/HC`) ou `OUTROS`.

## 4.4 Selectors e validadores

- Selectors (`src/cadastro/selectors/*`):
  - `listar_centros_ativos`, `listar_subcentros`, `obter_caminho_hierarquico`, `listar_centros_raiz`.
  - `listar_clientes_com_os`, `listar_intervencoes_com_os`, `listar_colaboradores_com_os`, `listar_funcoes_com_colaboradores`.
  - Função principal: encapsular queries com `annotate`, ordenação e `prefetch`.
- Validadores (`src/cadastro/validators/*`):
  - `validar_hierarquia_circular(tag)`: impede loop pai-filho.
  - `validar_codigo_unico(codigo, cliente_id=None)`: unicidade de código de cliente.
  - `validar_horarios_outros(colaborador)`: horários obrigatórios no turno `OUTROS`.

## 4.5 Views (`src/cadastro/views/*`)

- `cadastro_cliente` / `excluir_cliente`
  - CRUD de cliente com mensagens de sucesso/erro.
- `cadastrar_centro_custo`
  - Tela unificada de inclusão, edição e exclusão de ativos.
  - Integra service + árvore hierárquica para renderização.
- `cadastro_intervencao` / `excluir_intervencao`
  - CRUD com validação e feedback.
- `cadastro_funcao` / `editar_funcao` / `excluir_funcao`
  - CRUD da função de colaborador e proteção para exclusão em uso.
- `cadastro_colaborador` / `editar_colaborador` / `alternar_status_colaborador_view`
  - Cadastro/edição + ativação/desativação sem hard delete.

## 4.6 Utilitário de árvore

- `montar_hierarquia(centros)` (`src/cadastro/utils/centro_custo_tree.py`)
  - Converte queryset hierárquico em estrutura recursiva para template.

---

## 5. Módulo `abertura_os`

## 5.1 Modelos (`src/abertura_os/models/*`)

- `AberturaOS`
  - Entidade principal da OS com status `AB` (ativa) e `FI` (finalizada).
  - `gerar_proximo_numero_os()`:
    - gera sequencial anual no formato `NNN-AA`.
  - `save()`:
    - se `numero_os` vazio, gera automaticamente em transação.
- `FinalizacaoOS`
  - Dados técnicos de encerramento da OS (avaria, causa, sintoma, período e observações).
  - `clean()` valida consistência de intervalo início/fim.
- `PecaAplicada`
  - Itens aplicados na finalização, vinculados a `FinalizacaoOS`.

## 5.2 Forms (`src/abertura_os/forms.py`)

- `AberturaOSForm`
  - `__init__`: carrega somente clientes ativos e aplica classe visual nos widgets.
  - `clean_ssm`: SSM obrigatório e mínimo de tamanho.
  - `clean`: regra de incompatibilidade entre motivo e cliente (`SEM_CLIENTE`).
- `FinalizacaoOSForm`
  - configura widgets de texto/data e valida fim >= início.
- `PecaAplicadaForm` + `PecaAplicadaFormSet`
  - permite inserir várias peças aplicadas em bloco com `inlineformset`.

## 5.3 Service, selectors e queries

- `AberturaOSService._obter_centro_custo(centro_id)`
  - valida presença e existência do centro de custo.
- `AberturaOSService.criar_os(form, centro_id)`
  - grava OS nova com status aberto.
- `AberturaOSService.atualizar_os(form, centro_id)`
  - atualiza OS existente.
- `AberturaOSService.listar_ordens()`
  - listagem ordenada por data de abertura.
- `AberturaOSService.finalizar_os(os)`
  - troca situação para finalizada.
- Selectors:
  - `listar_os_ativas`, `listar_todas_os`.
- Queries auxiliares de centro de custo:
  - `get_centros_pais`, `get_subcentros`.

## 5.4 Views (`src/abertura_os/views/*`)

- `abrir_os`
  - Exibe preview do próximo número e realiza criação de OS.
- `editar_os`
  - Edição de OS existente com reaproveitamento da mesma tela.
- `excluir_os`
  - Remove OS por PK.
- `finalizar_os_view`
  - Fluxo completo de finalização:
    1. valida número da OS,
    2. impede finalizar OS já finalizada,
    3. valida form principal + formset de peças,
    4. salva finalização e peças em transação,
    5. atualiza observação/status na OS.
- `imprimir_os`
  - Renderiza template de impressão comum ou editável (query param `editavel=1`).
- `get_subcentros_ajax`
  - Endpoint JSON para carregamento dinâmico de subcentros.

## 5.5 Utilitários críticos (`src/abertura_os/utils/*`)

- `finalizar_ordem(numero_os, observacoes)`
  - utilitário simples para finalizar por número de OS.
- `gerar_pdf_imprimir_os(ordem_servico)`
  - gera PDF com campos editáveis (AcroForm) e layout corporativo.
  - Trechos-chave:
    - `_draw_label_value`, `_draw_section_title`: cabeçalhos e metadados.
    - `_draw_multiline_field`, `_draw_text_field`: campos editáveis.

---

## 6. Módulo `lancamento_horas`

## 6.1 Modelo (`src/lancamento_horas/models/apontamento_horas.py`)

- `ApontamentoHoras`
  - registra vínculo colaborador + OS + data/hora início/fim + tipo de dia.
  - `calcular_horas()` delega cálculo para serviço especializado.
  - `encerrar_aberto(...)` delega encerramento automático para serviço.

## 6.2 Serviço de cálculo (`src/lancamento_horas/services/apontamento_horas_service.py`)

- Métodos utilitários:
  - `_duracao_em_horas`, `_normalizar_datahora`, `_ajustar_para_referencia`.
- Regras de turno:
  - `obter_intervalos_turno(colaborador)` (A, B, HC, OUTROS).
- Classificação de data:
  - `classificar_tipo_dia(data)` retorna `Dia Normal`, `Sábado` ou `Dom/Feriado`.
- Cálculo principal:
  - `calcular_horas(apontamento)`
    - divide apontamento por dia,
    - identifica janelas normais do turno,
    - identifica intervalos de pausa,
    - calcula horas normais, extra 50% e extra 100%.
- Intervalos internos:
  - `_obter_intervalos_normais_no_dia`, `_obter_intervalos_pausa_no_dia`.
- Encerramento automático:
  - `_calcular_fim_turno_para_inicio` e `encerrar_aberto(...)`.
  - Se apontamento aberto é de outro dia, tenta encerrar no fim do turno.

## 6.3 Views

- `apontar_horas` (`src/lancamento_horas/views/apontar_horas.py`)
  - ação `iniciar`:
    - valida matrícula/OS,
    - bloqueia OS finalizada,
    - encerra apontamento aberto anterior quando necessário,
    - cria novo apontamento com `tipo_dia`.
  - ação `finalizar`:
    - busca apontamento aberto,
    - valida coerência de OS,
    - grava `data_fim`.
- `ajuste_horas` (`src/lancamento_horas/views/ajuste_horas.py`)
  - permite criar, editar e excluir ocorrências manualmente.
  - funções auxiliares importantes:
    - `_parse_datetime_local`: parse ISO com suporte a timezone.
    - `_ajustar_fim_virada_dia`: corrige intervalos que atravessam meia-noite.
    - `_intervalo_competencia`: competência operacional do dia 21 ao dia 20.
    - `_gerar_competencias`: lista competências disponíveis para filtro.
- APIs (`src/lancamento_horas/views/api.py`)
  - `api_colaborador`, `api_os`, `api_os_detalhes`: retornam dados JSON para preenchimento automático no frontend.

## 6.4 Utilitário de calendário (`src/lancamento_horas/utils/feriados.py`)

- `eh_feriado_ou_domingo(data)`
- `eh_sabado(data)`

São funções base para classificação de tipo de dia e cálculo de adicionais.

---

## 7. Módulo `relatorios`

## 7.1 Sequência de orçamento (`src/relatorios/models.py` e `src/relatorios/utils/orcamento.py`)

- `SequenciaOrcamento.proximo_numero(chave=...)`
  - usa transação + `select_for_update` para evitar colisão de sequência em concorrência.
- `ler_numero_orcamento()`
  - leitura sem incremento.
- `gerar_proximo_orcamento()`
  - incrementa e retorna próximo número.

## 7.2 Regras de relatório (`src/relatorios/utils/relatorio.py`)

- `formatar_moeda_br(valor)`
  - normaliza decimal e formata padrão BRL.
- `_calcular_segundos_com_desconto_pausas(apontamento, inicio, fim)`
  - subtrai pausas de turno para calcular tempo produtivo líquido.
- `processar_relatorio(apontamentos)`
  - agrega por função/colaborador,
  - converte horas em blocos (normal/50/100),
  - calcula custo com multiplicadores:
    - normal = 1.0x,
    - extra 50 = 1.5x,
    - extra 100 = 2.0x,
  - retorna linhas formatadas e totais.
- `construir_contexto_relatorio_os(request)`
  - monta contexto completo para tela de relatório por filtros (OS e período).
- `montar_dados_log_os(os_obj, data_inicio, data_fim)`
  - gera log detalhado por apontamento com duração líquida e totalizador final.

## 7.3 Utilitário de horário (`src/relatorios/utils/horario.py`)

- `formatar_horas`, `calcular_duracao`, `formatar_duracao`, `aplicar_filtro_datas`, `calcular_horas`.
- Observação: esse módulo contém funções genéricas; o cálculo principal do sistema utiliza `ApontamentoHorasService`.

## 7.4 Views (`src/relatorios/views/relatorios.py`)

- `relatorio_os`
  - tela principal dos relatórios.
- `orcamento_pdf`
  - prepara contexto consolidado e renderiza template de orçamento técnico.
- `proximo_orcamento`
  - endpoint JSON para número de orçamento.
- `log_os`
  - renderiza log completo da OS com filtros de data.
- `log_os_pdf`
  - versão PDF/print do log para emissão formal.

---

## 8. Trechos de código críticos (alto impacto)

1. **Geração de número da OS (`AberturaOS.gerar_proximo_numero_os` + `save`)**
   - Impacto direto na rastreabilidade e unicidade de ordens.
   - Deve ser testado sob cenários de concorrência e troca de ano.

2. **Timeout de sessão (`SessionTimeoutMiddleware`)**
   - Segurança e UX de autenticação.
   - Qualquer ajuste exige validar políticas diferentes por papel (`Fabrica` x demais).

3. **Cálculo de horas (`ApontamentoHorasService.calcular_horas`)**
   - Núcleo de cálculo de custo e relatório.
   - Trata virada de dia, pausas e distinção normal/extra.

4. **Finalização de OS com peças (`finalizar_os_view`)**
   - Fluxo transacional envolvendo múltiplas tabelas.
   - Falhas parciais devem sempre reverter via atomicidade.

5. **Sequência transacional de orçamento (`SequenciaOrcamento.proximo_numero`)**
   - Evita duplicidade de número sob múltiplas requisições simultâneas.

6. **Exclusão de ativo com descendentes (`excluir_centro_custo`)**
   - Regras de integridade de árvore + bloqueio por dependência de OS.

---

## 9. Matriz resumida de rotas por domínio

- `config/urls.py`: roteamento raiz.
- `dashboard/urls.py`: dashboard.
- `cadastro/urls.py`: ativos, clientes, intervenções, colaboradores e funções.
- `abertura_os/urls.py`: abrir/editar/excluir/finalizar/imprimir OS.
- `lancamento_horas/urls.py`: apontar, ajustar e APIs auxiliares.
- `relatorios/urls.py`: relatórios, logs e orçamento.

Todas as rotas de domínio estão protegidas por `role_required(...)` com listas explícitas de papéis permitidos.

---

## 10. Checklist de manutenção por alteração

1. Validar impacto da mudança em **services** e **relatórios**.
2. Confirmar permissões em `urls.py` com `role_required`.
3. Executar migrações quando alterar model.
4. Revalidar cálculos de horas (normal/50/100) em cenário de virada de dia.
5. Testar fluxo completo de OS: abrir → apontar → finalizar → relatar.