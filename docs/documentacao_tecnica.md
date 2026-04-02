# Documentação Técnica — Gestor OS (Nível SaaS Profissional)

> Objetivo: servir como guia **sênior, prático e conciso** para manutenção e evolução contínua do sistema.

## 1) Visão executiva do sistema

O Gestor OS é uma aplicação Django para operação industrial com cinco macrodomínios:

1. **Cadastro** (centro de custo, cliente, intervenção, colaborador e função).
2. **Abertura de OS** (ciclo de vida da ordem de serviço).
3. **Lançamento de horas** (apontamento de início/fim por colaborador).
4. **Relatórios** (custos por função, log de horas e orçamento em PDF).
5. **Dashboard + Controle de acesso por papéis (RBAC)**.

A aplicação usa:
- Django 6 + SQLite por padrão local.
- Templates server-side (Django Templates).
- Serviços e utilitários para regras de negócio (evitando acoplamento total nas views).

---

## 2) Arquitetura e fluxo macro

## 2.1 Entradas HTTP (roteamento raiz)

Todas as rotas entram por `config/urls.py`, que distribui para os apps.

- `login/`, `logout/`
- `cadastro/`
- `abertura_os/`
- `lancamento_horas/`
- `relatorios/`

## 2.2 Camadas por responsabilidade

Padrão efetivo do projeto:

- **View**: recebe request, valida fluxo de tela e mensagens ao usuário.
- **Form**: valida campos de entrada com regras de UI e consistência.
- **Service**: regra de negócio reutilizável (criar/editar/finalizar/cálculo).
- **Model**: persistência + regras essenciais de entidade.
- **Utils/Selectors/Queries**: funções de apoio, consultas especializadas e montagem de dados para relatório.

---

## 3) Mapa técnico por módulo

## 3.1 `config` (core da aplicação)

### O que faz
- Centraliza configuração do Django (`settings.py`).
- Define roteamento principal (`urls.py`).
- Implementa autenticação (`auth_views.py`) e autorização por grupos (`access_control.py`).

### Como faz
- Regra de papéis fixos: `ADM`, `PCM`, `Supervisor`, `Almoxarife`, `Fabrica`.
- Decorador `role_required(...)` protege views por grupo.
- `ensure_roles_exist()` garante criação automática dos grupos no banco.

### Manutenção rápida
1. Para criar novo perfil, adicione constante em `access_control.py` e inclua em `ALL_ROLES`.
2. Atualize as rotas que exigem esse perfil (`role_required`).
3. Ajuste cards do dashboard para exibir funcionalidade ao novo papel.

---

## 3.2 `dashboard`

### O que faz
- Página inicial pós-login, com cards por categoria (OS, Cadastros, Relatórios).

### Como faz
- Monta `categorias` com `roles` permitidos por card.
- Filtra em runtime com `user_has_any_role(...)`.

### Ponto de atenção
- Existe um typo no `login_view`: `redirect("deshboard")` quando já autenticado. Corrigir para `dashboard` evita erro de rota.

---

## 3.3 `cadastro`

### O que faz
- Mantém entidades mestre do domínio.

### Modelos principais
- **CentroCusto**: árvore via auto-relacionamento (`centro_pai`), com `on_delete=PROTECT`.
- **Cliente**: código único e indicador `ativo`.
- **Intervencao**: código e descrição únicos.
- **Colaborador**: matrícula única, turno e horários customizáveis para turno `OUTROS`.
- **Funcao_colab**: base de função/custo hora usada em relatórios.

### Como faz
- Serviços por contexto (`cliente_service`, `colaborador_service`, etc.).
- Validadores específicos de domínio para dados críticos (cliente, centro de custo, colaborador).

### Manutenção rápida
- Nova regra de cadastro: priorize implementar no **validator/service** e manter view “fina”.
- Alterações de modelo: crie migração e valide impacto nas FKs protegidas (`PROTECT`).

---

## 3.4 `abertura_os`

### O que faz
- Cria, edita, exclui, imprime e finaliza ordens de serviço.

### Como faz
- `AberturaOS` contém a regra de numeração automática `NNN-AA` em `save()`.
- `AberturaOSService` encapsula criação, atualização, listagem e finalização.
- `AberturaOSForm` valida SSM e regras de cliente x motivo de intervenção.

### Fluxo principal (abrir OS)
1. View `abrir_os` exibe preview do próximo número.
2. POST valida formulário.
3. Service resolve centro de custo e salva entidade.
4. Modelo gera número automaticamente se vazio.

### Manutenção rápida
- Mudança no formato da OS: alterar `gerar_proximo_numero_os()` e testar concorrência.
- Nova validação de abertura: implementar no form (`clean`/`clean_<campo>`).

---

## 3.5 `lancamento_horas`

### O que faz
- Registra início/fim de apontamentos por colaborador e OS.
- Expõe APIs auxiliares para frontend (consulta colaborador/OS).

### Como faz
- `apontar_horas` controla início/fim com mensagens de negócio.
- Bloqueia apontamento em OS finalizada.
- Se já houver apontamento aberto, tenta encerramento automático (`encerrar_aberto`).
- `ApontamentoHorasService` calcula horas normais/50%/100% considerando:
  - tipo do dia (normal, sábado, domingo/feriado),
  - intervalos de turno,
  - pausas entre blocos de turno,
  - virada de data e timezone (naive vs aware).

### Fluxo principal (iniciar apontamento)
1. Validar matrícula e status ativo do colaborador.
2. Validar número da OS e se está aberta.
3. Encerrar apontamento aberto anterior, quando aplicável.
4. Classificar tipo de dia e criar registro com `data_inicio`.

### Fluxo principal (finalizar apontamento)
1. Buscar apontamento aberto do colaborador.
2. Validar consistência com OS informada.
3. Definir `data_fim` com horário atual e persistir.

### Manutenção rápida
- Nova regra de hora extra: ajustar apenas `ApontamentoHorasService.calcular_horas`.
- Nova escala de turno: adicionar em `obter_intervalos_turno`.

---

## 3.6 `relatorios`

### O que faz
- Consolida horas/custos e gera páginas/PDFs de orçamento e log de OS.

### Como faz
- `processar_relatorio(...)` agrega horas por função e calcula financeiro:
  - normal = 1.0x
  - extra 50 = 1.5x
  - extra 100 = 2.0x
- `montar_dados_log_os(...)` gera linhas detalhadas por colaborador com desconto de pausas.
- `orcamento.py` controla número sequencial em arquivo (`controle_orcamento.txt`).

### Manutenção rápida
- Se migrar para múltiplas instâncias (SaaS real), substituir sequência em arquivo por tabela com lock transacional.
- Para novos relatórios, reutilizar pipeline: `queryset -> processar -> context -> template`.

---

## 3.7 Gestão de sessão e segurança (timeout)

### Regras implementadas
- **Todos os usuários (exceto grupo `Fabrica`)**: logout automático após **10 minutos sem interação**.
- **Aviso visual de expiração**: contador regressivo aparece quando faltam **2 minutos** para encerrar a sessão por inatividade.
- **Grupo `Fabrica`**: exceção de política, com sessão de **8 horas contínuas** (timeout absoluto), sem corte por inatividade de 10 minutos.

### Componentes técnicos
- `config/session_policy.py`: centraliza constantes e políticas de sessão.
- `config/middleware.py` (`SessionTimeoutMiddleware`): valida timeout por request autenticada e encerra sessão quando aplicável.
- `config/context_processors.py`: injeta configuração de timeout no template.
- `templates/base.html` + `config/static/js/session_timeout.js`: exibição do banner e cronômetro regressivo no frontend.
- `config/auth_views.py`: inicializa timestamps de sessão no login e exibe mensagens claras na tela de autenticação ao expirar.

---
## 4) Guia de manutenção (passo a passo dinâmico)

## 4.1 Setup local rápido

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 4.2 Checklist antes de alterar código

1. Identifique o domínio (`cadastro`, `abertura_os`, `lancamento_horas`, `relatorios`).
2. Localize a camada certa da regra (view/form/service/model).
3. Verifique permissão da rota (`role_required`).
4. Avalie impacto em relatórios/cálculos de horas.
5. Rode migrações/testes após alteração.

## 4.3 Playbook: criar nova funcionalidade

1. Criar/ajustar model (se necessário).
2. Criar migration.
3. Implementar service com regra central.
4. Expor view + rota.
5. Integrar template/frontend.
6. Aplicar controle de acesso por perfil.
7. Cobrir com teste de serviço e teste de view.

## 4.4 Playbook: corrigir bug de produção

1. Reproduzir com dados reais/similares.
2. Isolar camada de falha (entrada, regra, persistência, template).
3. Corrigir no ponto certo (evitar workaround em view se a regra é de service).
4. Escrever teste de regressão.
5. Validar manualmente fluxo completo.

---

## 5) Explicação dos códigos críticos (o que faz e como faz)

## 5.1 Controle de acesso (`config/access_control.py`)
- **O que faz:** controla autorização por grupos.
- **Como faz:** wrapper `role_required` combina `login_required` + validação por grupo + feedback via `messages`.

## 5.2 Numeração de OS (`abertura_os/models/abertura_os.py`)
- **O que faz:** gera número incremental anual no formato `001-26`.
- **Como faz:** busca último número do ano e incrementa no `save` quando `numero_os` está vazio.

## 5.3 Cálculo de horas (`lancamento_horas/services/apontamento_horas_service.py`)
- **O que faz:** separa horas normais, extra 50 e extra 100.
- **Como faz:** divide período em blocos por dia, cruza com janelas de turno e desconta pausas.

## 5.4 Fechamento automático de apontamento aberto
- **O que faz:** evita apontamento “pendurado” entre dias.
- **Como faz:** ao iniciar nova OS, tenta fechar apontamento anterior no fim do turno (ou no horário atual se mesmo dia).

## 5.5 Sequência de orçamento (`relatorios/utils/orcamento.py`)
- **O que faz:** gera número sequencial de orçamento.
- **Como faz:** lê arquivo texto e incrementa contador.
- **Melhoria SaaS recomendada:** mover para banco com transação para evitar conflito em concorrência.

---

## 6) Roadmap técnico de melhorias (nível sênior / SaaS)

Prioridade alta:
1. **Segurança**
   - Remover `DEBUG=True` em produção.
   - Externalizar `SECRET_KEY` e credenciais via variáveis de ambiente.
   - Restringir `ALLOWED_HOSTS`.
2. **Banco de dados**
   - Migrar SQLite para PostgreSQL em produção.
3. **Observabilidade**
   - Estruturar logging por domínio (abertura_os, lancamento_horas, relatorios).
4. **Qualidade**
   - Expandir testes automatizados para services críticos (horas e OS).
5. **Escalabilidade**
   - Substituir sequência de arquivo por tabela/serviço transacional.

Prioridade média:
1. Versionar API interna de apoio ao frontend.
2. Introduzir camada de permissions por ação (além de role global).
3. Criar documentação de contratos de dados (campos por endpoint).

---

## 7) Padrão de contribuição recomendado

- Sempre separar PRs por domínio (evitar PR “monolítico”).
- Regra de negócio em `services/`.
- Validação de formulário em `forms.py`.
- View focada em orquestração e resposta HTTP.
- Nomear funções com verbo + contexto (`criar_os`, `finalizar_os`, `calcular_horas`).

---

## 8) Runbook rápido de incidentes

## 8.1 Usuário não vê card no dashboard
1. Conferir grupo do usuário no admin.
2. Conferir roles no card em `dashboard_views.py`.
3. Conferir proteção da rota via `role_required`.

## 8.2 Erro ao iniciar apontamento
1. Validar matrícula ativa.
2. Validar OS aberta e existente.
3. Verificar apontamento aberto antigo bloqueando.

## 8.3 Total de relatório inconsistente
1. Conferir `data_inicio`/`data_fim` do filtro.
2. Verificar se há apontamentos sem `data_fim`.
3. Validar função/valor_hora do colaborador.

---

## 9) Conclusão

Esta documentação foi estruturada para operação **rápida**, **didática** e com foco em **manutenção ágil** e **evolução SaaS profissional**.

Se quiser, o próximo passo pode ser criar uma **Matriz de Impacto por Módulo** (arquivo adicional) para acelerar onboarding de novos devs e reduzir risco de regressão em deploy.