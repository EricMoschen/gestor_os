# Documentação Técnica Completa — Gestor OS

---

## 1) Visão geral do produto

O **Gestor OS** é um sistema web Django para gestão de manutenção/operação industrial, cobrindo o fluxo completo de:

1. **Cadastros mestre** (cliente, centro de custo, intervenção, colaborador, função).
2. **Abertura e ciclo de vida de OS**.
3. **Lançamento de horas por colaborador e OS**.
4. **Relatórios e orçamentos em PDF**.
5. **Acesso por perfil e dashboard por permissões**.

Em arquitetura, trata-se de um **monólito modular** (apps Django separados por domínio), com templates server-side e regras de negócio distribuídas em views/forms/services/utils.

---

## 2) Tecnologias e stack

### Backend
- **Python**
- **Django** (aplicação principal)
- ORM nativo Django

### Banco de dados
- **SQLite** em desenvolvimento local (padrão atual).
- Recomendado em produção: **PostgreSQL**.

### Frontend
- Django Templates
- JavaScript e CSS por módulo

### Geração de documentos
- Relatórios/orçamentos em PDF (com utilitários e templates específicos)

---

## 3) Estrutura de diretórios (visão para manutenção)

```text
manage.py
src/
  config/               # Configurações globais, urls raiz, auth, middleware, RBAC
  dashboard/            # Página inicial pós-login
  cadastro/             # Entidades mestre e seus fluxos de cadastro
  abertura_os/          # Fluxo operacional da ordem de serviço
  lancamento_horas/     # Apontamento e cálculo de horas
  relatorios/           # Consolidação de dados e PDFs
  templates/            # Base compartilhada da UI

docs/
  documentacao_tecnica.md
  implementacao.md
  usabilidade_usuario.md
  matriz_impacto_modulo.md
```

---

## 4) Arquitetura lógica e responsabilidades

## 4.1 Roteamento principal
O ponto de entrada HTTP é o roteamento global em `config/urls.py`, que delega as rotas para cada app.

## 4.2 Padrão de separação de responsabilidades
No estado atual do projeto, o padrão recomendado para evoluções é:

- **Views:** orquestram request/response, mensagens e redirecionamentos.
- **Forms:** validação de entrada e regras de consistência de formulário.
- **Services:** regras de negócio reutilizáveis e processamento principal.
- **Models:** entidades persistidas e regras essenciais da entidade.
- **Selectors/Utils/Validators:** consultas especializadas, cálculos e validações de domínio.

Esse padrão reduz acoplamento, facilita teste e evita “engordar” views.

---

## 5) Módulos do sistema (detalhado)

## 5.1 `config` (núcleo da aplicação)

### Responsabilidade
- Configuração global do Django.
- Autenticação de usuário e sessão.
- Controle de acesso baseado em papéis.

### Pontos importantes
- Define políticas de sessão (incluindo timeout e comportamento por perfil).
- Mantém papéis de acesso (ex.: `ADM`, `PCM`, `Supervisor`, `Almoxarife`, `Fabrica`) via utilitário de controle de acesso.
- Concentra middleware/context processors relevantes ao funcionamento global.

### Riscos comuns de manutenção
- Alterações em middleware podem afetar todo o sistema.
- Mudanças em RBAC podem ocultar menus/rotas sem erro explícito de backend.

### Checklist ao alterar
- Validar login/logout.
- Validar acesso por perfil em ao menos 1 rota por domínio.
- Validar timeout de sessão.

---

## 5.2 `dashboard`

### Responsabilidade
- Tela inicial após autenticação.
- Exibir atalhos/cards conforme permissão.

### Riscos comuns
- Divergência entre card exibido e permissão real da rota.
- Quebra de navegação por nome de rota incorreto.

### Checklist ao alterar
- Conferir renderização por perfil.
- Conferir redirecionamentos e nomes de URL.

---

## 5.3 `cadastro`

### Responsabilidade
Módulo de dados mestre, base para quase todos os outros fluxos:
- Centro de custo
- Cliente
- Intervenção
- Colaborador
- Função de colaborador

### Componentes importantes
- `models/`: entidades e relacionamentos.
- `forms.py`: validações de entrada.
- `validators/`: regras específicas de domínio.
- `selectors/`: consultas reutilizáveis.
- `views/`: fluxo de telas e operações.

### Regras de negócio típicas
- Unicidade de códigos/matrículas.
- Controle de ativos/inativos.
- Integridade de relacionamento entre entidades.

### Riscos comuns
- Mudança em cadastro impacta abertura de OS, horas e relatórios.
- Quebra de FK/relacionamentos gera erros em cascata.

### Checklist ao alterar
- Executar CRUD completo da entidade alterada.
- Testar comportamento com registro inativo.
- Testar impacto em fluxo que consome essa entidade.

---

## 5.4 `abertura_os`

### Responsabilidade
- Abrir, editar, finalizar, excluir e imprimir ordens de serviço.
- Controlar o ciclo de vida da OS.

### Componentes importantes
- Model de OS e regras de numeração/status.
- Form com validações de consistência.
- Service para regra de negócio de criação/finalização.

### Regras críticas
- Numeração de OS (incremental por padrão vigente).
- Bloqueio/validação de ações quando OS está finalizada.

### Riscos comuns
- Qualquer mudança de status da OS impacta apontamento de horas.
- Mudanças de numeração afetam rastreabilidade e auditoria.

### Checklist ao alterar
- Criar OS.
- Editar OS.
- Finalizar OS.
- Validar bloqueios pós-finalização.
- Conferir impressão/exportação.

---

## 5.5 `lancamento_horas`

### Responsabilidade
- Registrar início e fim de apontamentos por colaborador/OS.
- Calcular distribuição de horas normais e extras.
- Disponibilizar informações auxiliares para frontend.

### Componentes importantes
- `models/apontamento_horas.py`
- `views/apontar_horas.py`
- serviços/utilitários de cálculo (incluindo feriados e regras de turno)

### Regras críticas
- Não permitir apontar em OS finalizada.
- Encerrar apontamento aberto quando necessário (regra de consistência operacional).
- Cálculo de horas com tratamento de intervalos/turnos e tipo de dia.

### Riscos comuns
- Erros de cálculo geram impacto financeiro direto em relatório/orçamento.
- Erros de timezone/data podem distorcer apuração em bordas de dia/turno.

### Checklist ao alterar
- Iniciar apontamento válido.
- Finalizar apontamento válido.
- Bloqueio com OS finalizada.
- Cenário de apontamento já aberto.
- Conferência de horas (normal, 50%, 100%).
- Validar responsividade mobile da tela de apontamento (formulário e listagem de OS em cards).

---

## 5.6 `relatorios`

### Responsabilidade
- Consolidar dados operacionais.
- Gerar relatórios gerenciais e documentos PDF (orçamento e log).

### Componentes importantes
- `views/relatorios.py`
- `utils/relatorio.py`
- `utils/orcamento.py`
- templates e CSS de PDF

### Regras críticas
- Agregação de horas por função/período.
- Cálculo de custo com multiplicadores (normal, 50, 100).
- Sequência de orçamento persistida em arquivo (modelo atual).

### Riscos comuns
- Dado inconsistente no relatório = decisão operacional/financeira errada.
- Sequência em arquivo pode ter conflito em cenários concorrentes (produção escalada).

### Checklist ao alterar
- Validar totalizadores por função.
- Validar filtros de período.
- Validar renderização PDF.
- Validar consistência com lançamentos de horas.

---

## 6) Fluxos ponta a ponta mais importantes

## 6.1 Fluxo A — Preparação de base
1. Cadastrar centro de custo.
2. Cadastrar cliente.
3. Cadastrar intervenção.
4. Cadastrar função e colaborador.

## 6.2 Fluxo B — Execução operacional
1. Abrir OS.
2. Iniciar apontamento de horas.
3. Finalizar apontamento.
4. Finalizar OS.

## 6.3 Fluxo C — Consolidação gerencial
1. Filtrar período/OS no módulo de relatórios.
2. Conferir totais de horas.
3. Gerar orçamento/log em PDF.

---

## 7) Modelo de dados (visão funcional)

Entidades centrais do domínio:
- **Cliente**
- **Centro de Custo**
- **Intervenção**
- **Colaborador**
- **Função do colaborador**
- **Abertura OS**
- **Apontamento de Horas**

Relacionamentos (conceitual):
- Uma OS referencia cliente, centro de custo e intervenção.
- Apontamentos de horas referenciam colaborador e OS.
- Relatórios consolidam dados de apontamentos + função/valor-hora.

Para visão complementar de tabelas, consultar `docs/arquitetura_tabelas/`.

---

## 8) Controle de acesso e sessão

### RBAC (papéis)
Os módulos e ações são protegidos por grupos/perfis. O padrão de manutenção é:
1. Criar/ajustar papel em camada de controle de acesso.
2. Aplicar proteção de rota/view.
3. Ajustar dashboard/menu para refletir a permissão.

### Sessão
Há política de timeout com comportamento específico por perfil, com destaque para exceções operacionais (ex.: perfil de chão de fábrica).

--

## 9) Qualidade e testes

## 9.1 O que deve ser testado sempre
- Login e acesso por perfil.
- Cadastro base.
- Abertura/finalização de OS.
- Início/fim de apontamento.
- Relatório com totalizadores e PDF.

## 9.2 Estratégia recomendada
- **Teste unitário:** services e utilitários de cálculo.
- **Teste de integração:** view + model + persistência.
- **Teste funcional:** fluxo ponta a ponta em ambiente de homologação.

## 9.3 Casos de regressão prioritários
- Cálculo de hora extra (50/100).
- Encerramento automático de apontamento aberto.
- Regras de bloqueio em OS finalizada.
- Diferença de total entre tela e PDF.
