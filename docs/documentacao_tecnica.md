# Documentação Técnica — Gestor OS

Atualizada com base na estrutura e nas regras presentes no código-fonte atual.

---

## 1) Visão geral

O **Gestor OS** é um monólito modular em Django para operação de manutenção. O sistema cobre:

1. cadastro de dados mestre;
2. abertura, edição, impressão, exclusão e finalização de ordens de serviço;
3. apontamento e ajuste de horas por colaborador e OS;
4. consolidação de horas, logs e orçamentos;
5. autenticação, sessão, tema visual e acesso por papéis.

A aplicação usa templates Django renderizados no servidor, com arquivos CSS/JS separados por módulo.

---

## 2) Stack e configuração

### 2.1 Tecnologias

- **Python** e **Django 6**.
- **SQLite** quando `DATABASE_URL` não está configurada.
- **Banco externo via `DATABASE_URL`** em produção, usando `dj-database-url` com SSL obrigatório nos settings de produção.
- **WhiteNoise** para servir estáticos coletados.
- **Gunicorn** como servidor WSGI no deploy.
- Bibliotecas de PDF/documentos presentes nas dependências: `weasyprint`, `reportlab`, `pydyf`, `pypandoc`, `python-docx`.

### 2.2 Settings por ambiente

O módulo de settings é `src.config.settings` e escolhe o arquivo conforme `DJANGO_ENV`:

- `development` (padrão): `DEBUG=True` e `ALLOWED_HOSTS=["*"]`.
- `production`: `DEBUG=False`, banco por `DATABASE_URL`, HTTPS/secure cookies e `SECURE_SSL_REDIRECT=True`.
- `test`: `DEBUG=False` e hasher MD5 para acelerar testes.

Variáveis relevantes:

| Variável | Uso |
| --- | --- |
| `DJANGO_ENV` | Seleciona `development`, `production` ou `test`. |
| `DJANGO_SECRET_KEY` / `SECRET_KEY` | Chave secreta. |
| `DJANGO_ALLOWED_HOSTS` | Lista separada por vírgula. |
| `DATABASE_URL` | Banco de dados externo. |
| `DJANGO_SUPERUSER_USERNAME` | Usuário para `ensure_superuser`. |
| `DJANGO_SUPERUSER_PASSWORD` | Senha para `ensure_superuser`. |
| `DJANGO_SUPERUSER_EMAIL` | E-mail opcional do superusuário. |

---

## 3) Estrutura de diretórios

```text
manage.py
render.yaml
requirements.txt
src/
  config/               # settings, URLs raiz, autenticação, RBAC, sessão, tema
  dashboard/            # tela inicial pós-login
  cadastro/             # dados mestre e validações de domínio
  abertura_os/          # ciclo de vida da ordem de serviço
  lancamento_horas/     # apontamento, APIs e ajuste de horas
  relatorios/           # relatórios, logs e orçamentos
  templates/            # base e componentes compartilhados

docs/
  documentacao_tecnica.md
  documentacao_tecnica_detalhada.md
  implementacao.md
  usabilidade_usuario.md
  arquitetura_tabelas/
```

---

## 4) Roteamento HTTP

### 4.1 Rotas raiz (`src.config.urls`)

| Caminho | Destino |
| --- | --- |
| `/login/` | Login customizado. |
| `/logout/` | Logout customizado. |
| `/preferencias/tema/` | Atualização de tema visual do usuário. |
| `/admin/` | Admin Django. |
| `/` | Dashboard. |
| `/cadastro/` | URLs do módulo de cadastro. |
| `/abertura_os/` | URLs do módulo de OS. |
| `/lancamento_horas/` | URLs de apontamento/ajuste. |
| `/relatorios/` | URLs de relatórios. |

### 4.2 Permissões por módulo

Papéis existentes: `ADM`, `PCM`, `Supervisor`, `Almoxarife`, `Fabrica`.

| Área | Papéis com acesso |
| --- | --- |
| Centro de custo/ativos | `ADM`, `PCM`, `Almoxarife` |
| Clientes | `ADM`, `Almoxarife` |
| Intervenções | `ADM`, `PCM`, `Almoxarife` |
| Colaboradores | `ADM`, `Supervisor`, `Almoxarife` |
| Funções | `ADM`, `Supervisor`, `Almoxarife` |
| Abertura/edição/exclusão/finalização/impressão de OS | `ADM`, `PCM`, `Almoxarife` |
| Apontar horas e APIs auxiliares | `ADM`, `Supervisor`, `Almoxarife`, `Fabrica` |
| Ajustar horas | `ADM`, `Supervisor`, `Almoxarife` |
| Relatórios e PDFs | `ADM`, `Supervisor`, `Almoxarife` |

Superusuários passam por todas as verificações de papel.

---

## 5) Núcleo `config`

### 5.1 Autenticação e bootstrap de grupos

- O login garante a criação dos grupos padrão antes de autenticar.
- Usuário já autenticado é redirecionado ao dashboard.
- Credenciais inválidas exibem mensagem de erro.
- O logout aceita motivo de timeout para exibir mensagem amigável na tela de login.

### 5.2 Sessão

Políticas atuais:

| Política | Usuários | Inatividade | Aviso | Timeout absoluto |
| --- | --- | --- | --- | --- |
| `default` | Demais perfis | 10 minutos | 2 minutos antes | Não configurado no código atual |
| `fabrica` | Grupo `Fabrica` | Sem timeout idle | Não aplicável | 12 horas |

O middleware ignora usuários anônimos e as rotas de login/logout, aplica timeout absoluto quando configurado e atualiza `last_activity_ts` a cada request autenticada válida.

### 5.3 Tema visual

O projeto possui contexto `user_theme` e rota `/preferencias/tema/` para persistir preferência visual do usuário autenticado.

### 5.4 Comando operacional

`python manage.py ensure_superuser` cria ou atualiza um superusuário usando variáveis de ambiente. Em produção, ausência de usuário/senha ou senha inválida gera erro; fora de produção, gera aviso.

---

## 6) Módulo `cadastro`

### 6.1 Entidades

- `CentroCusto`: ativo/centro hierárquico com `cod_centro` como chave primária, `tenant_id`, `cod_tag`, descrição, pai opcional, código do ativo e status ativo. Há unicidade condicional de `cod_tag` por tenant.
- `Cliente`: código único, nome, timestamps e status ativo.
- `Intervencao`: código numérico único e descrição única.
- `Funcao_colab`: descrição única e valor-hora.
- `Colaborador`: matrícula única de 4 caracteres, nome, status, função protegida, turno e horários customizados.

### 6.2 Regras e serviços

- Centros de custo podem formar árvore pai/filho, com validação contra hierarquia circular.
- Exclusão de centro bloqueia quando há OS vinculada ao centro ou descendentes.
- Cliente valida código único e pode ser ativado/desativado pelo campo `ativo`.
- Intervenção gera código incremental no serviço e bloqueia remoção quando há OS vinculada.
- Colaborador com turno `OUTROS` exige quatro horários no formulário/modelo.
- Colaborador não é removido fisicamente pela tela principal; o fluxo alterna `ativo`.
- Horários padrão: turno A, B, HC e OUTROS são resolvidos por `HorarioService` e pelo serviço de apontamento.

---

## 7) Módulo `abertura_os`

### 7.1 Modelo de OS

`AberturaOS` contém:

- `numero_os` único, gerado automaticamente;
- descrição;
- centro de custo obrigatório;
- cliente opcional;
- motivo de intervenção obrigatório;
- SSM;
- situação `AB`/`FI`;
- data de abertura;
- observações.

A numeração atual usa formato `NNNN-AA`, por exemplo `0001-26`, reiniciando a sequência por ano com base no sufixo do ano.

### 7.2 Finalização

`FinalizacaoOS` possui vínculo um-para-um com a OS e registra avaria, intervenção, sintoma, causa, início/fim e observações. `PecaAplicada` armazena itens aplicados na finalização.

Regras principais:

- fim deve ser maior ou igual ao início;
- OS já finalizada não deve ser finalizada novamente;
- finalização salva formulário principal e peças em transação;
- status da OS é alterado para `FI` após finalizar.

### 7.3 Fluxos expostos

- abrir OS com preview do próximo número;
- editar OS existente;
- excluir OS;
- buscar subcentros via AJAX;
- finalizar OS;
- imprimir OS comum ou editável via querystring `editavel=1`.

---

## 8) Módulo `lancamento_horas`

### 8.1 Modelo

`ApontamentoHoras` vincula colaborador e OS, com `data_inicio`, `data_fim` e `tipo_dia`.

### 8.2 Apontamento

A tela de apontamento e as APIs auxiliares permitem localizar colaborador por matrícula, localizar OS por número e consultar detalhes de OS.

Regras relevantes:

- colaborador precisa existir e estar ativo;
- OS precisa existir;
- OS finalizada é bloqueada para novos apontamentos;
- apontamento aberto anterior do colaborador pode ser encerrado pelo serviço;
- cálculo só retorna horas quando `data_fim` existe.

### 8.3 Cálculo de horas

O serviço classifica horas em:

- horas normais;
- horas extras 50%;
- horas extras 100%.

Regras implementadas:

- domingo e feriado contam como 100%;
- sábado conta como 50%, com regra especial para turno que cruza meia-noite;
- dias normais comparam o intervalo apontado contra intervalos do turno;
- pausas de turno são descontadas quando cobertas pelo apontamento;
- tolerância de 5 minutos ajusta início/fim próximos aos limites de turno;
- turnos A, B, HC e OUTROS são suportados;
- datas naive/aware são normalizadas para evitar erro de comparação.

### 8.4 Ajuste de horas

O módulo possui rota de ajuste acessível a `ADM`, `Supervisor` e `Almoxarife`, com template e JavaScript próprios.

---

## 9) Módulo `relatorios`

### 9.1 Funcionalidades

- relatório por OS com filtros;
- orçamento de horas;
- consulta do próximo número de orçamento;
- log de OS em tela de orçamento;
- relatório/orçamento do cliente.

### 9.2 Sequência de orçamento

A numeração de orçamento é controlada por `SequenciaOrcamento`, em banco de dados, com incremento dentro de transação e `select_for_update()`.

Observação importante: endpoints que chamam `gerar_proximo_orcamento()` consomem um número da sequência. Isso inclui geração/visualização de orçamento e consulta do próximo número.

### 9.3 Cálculo financeiro

Os relatórios consolidam apontamentos por colaborador/função e usam valor-hora da função para calcular totais por horas normais, 50% e 100%.

---

## 10) Fluxos ponta a ponta

### Fluxo A — Preparação da base

1. Cadastrar centros de custo/ativos.
2. Cadastrar clientes ativos.
3. Cadastrar intervenções.
4. Cadastrar funções com valor-hora.
5. Cadastrar colaboradores ativos e turnos.

### Fluxo B — Execução operacional

1. Abrir OS.
2. Apontar início/fim de horas.
3. Ajustar horas quando necessário.
4. Finalizar OS com dados técnicos e peças.
5. Imprimir OS quando necessário.

### Fluxo C — Consolidação gerencial

1. Filtrar OS/período em relatórios.
2. Conferir horas e totais.
3. Emitir orçamento/log/relatório para impressão/PDF.

---

## 11) Checklist de manutenção

Antes de entregar alterações, valide:

- `python manage.py check`;
- migrações pendentes (`python manage.py makemigrations --check --dry-run` quando aplicável);
- login/logout e timeout;
- permissões por pelo menos um usuário de cada papel afetado;
- CRUD ou fluxo da entidade alterada;
- abertura/finalização de OS quando mexer em cadastro, OS ou apontamento;
- cálculo normal/50%/100% quando mexer em horários ou feriados;
- renderização das telas e templates de orçamento quando mexer em relatórios.