# Gestor OS

Sistema web para gestão de ordens de serviço, apontamento de horas, cadastros operacionais e relatórios.

## Documentação completa

A documentação completa (instalação, módulos, ações, manutenção e usabilidade) está em:

- [`docs/documentacao_tecnica.md`](docs/documentacao_tecnica.md)
- [`docs/documentacao_tecnica_detalhada.md`](docs/documentacao_tecnica_detalhada.md)
- [`docs/usabilidade_usuario.md`](docs/usabilidade_usuario.md)
- [`docs/implementacao.md`](docs/implementacao.md)

## Execução rápida

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000/login/`.
