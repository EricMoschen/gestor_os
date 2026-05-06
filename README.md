# Gestor OS

Sistema web Django para gestão de ordens de serviço, cadastros operacionais, apontamento/ajuste de horas e relatórios/orçamentos.

## Stack atual

- Python + Django 6.
- Templates server-side, CSS e JavaScript por módulo.
- SQLite em desenvolvimento quando `DATABASE_URL` não está definida.
- Banco via `DATABASE_URL` com `dj-database-url` em produção.
- WhiteNoise para arquivos estáticos.
- Gunicorn no deploy Render.

## Módulos principais

- `config`: settings por ambiente, autenticação, logout por timeout, tema do usuário, RBAC e comando `ensure_superuser`.
- `dashboard`: entrada pós-login com cards conforme permissões.
- `cadastro`: centros de custo/ativos, clientes, intervenções, colaboradores e funções.
- `abertura_os`: abertura, edição, exclusão, finalização e impressão de OS.
- `lancamento_horas`: apontamento de horas, APIs auxiliares e ajuste manual.
- `relatorios`: relatório por OS, logs e geração de orçamento/relatório em HTML para impressão/PDF.

## Documentação completa

- [`docs/documentacao_tecnica.md`](docs/documentacao_tecnica.md): visão técnica atualizada pelo código.
- [`docs/documentacao_tecnica_detalhada.md`](docs/documentacao_tecnica_detalhada.md): detalhamento por módulo e componentes internos.
- [`docs/usabilidade_usuario.md`](docs/usabilidade_usuario.md): guia operacional para usuários.
- [`docs/implementacao.md`](docs/implementacao.md): instalação, deploy e runbook.
- [`docs/arquitetura_tabelas/definicao_tabelas.md`](docs/arquitetura_tabelas/definicao_tabelas.md): visão funcional das tabelas.