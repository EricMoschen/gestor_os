# Desenho de Pastas (SaaS)


gestor_os/
├── manage.py
├── requirements.txt
├── config/
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── auth_views.py
│   ├── access_control.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── development.py
│       ├── test.py
│       └── production.py
├── templates/
│   └── base.html
├── docs/
│   ├── DOCUMENTACAO_SAAS.md
│   ├── ARVORE_PASTAS_SAAS.md
│   ├── documentacao_tecnica.md
│   ├── implementacao.md
│   └── usabilidade_usuario.md
├── saas/
│   ├── iam/
│   │   ├── api/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── tests/
│   ├── tenancy/
│   │   ├── api/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── tests/
│   ├── billing/
│   │   ├── api/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── tests/
│   ├── observability/
│   │   ├── api/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── tests/
│   └── shared/
│       ├── api/
│       ├── services/
│       ├── repositories/
│       └── tests/
├── saas_platform/
│   ├── apps.py
│   ├── urls.py
│   ├── api/
│   │   └── v1/
│   ├── views/
│   │   └── health.py
│   ├── services/
│   │   └── system_status.py
│   ├── selectors/
│   ├── repositories/
│   └── tests/
│       └── test_health.py
├── dashboard/
├── cadastro/
├── abertura_os/
├── lancamento_horas/
└── relatorios/
```

## Fluxo de organização

- **Módulos legados de negócio**: `dashboard`, `cadastro`, `abertura_os`, `lancamento_horas`, `relatorios`
- **Camada SaaS de plataforma**: `saas_platform`
- **Domínios SaaS para expansão**: `saas/*`
- **Configuração por ambiente**: `config/settings/*`