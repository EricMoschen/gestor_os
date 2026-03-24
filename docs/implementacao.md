# Documentação de Implementação do Sistema 

> **Objetivo:** disponibilizar o `gestor_os` com padrão profissional de implantação, configuração e operação, com foco em previsibilidade, segurança e escalabilidade.

---

## 1) Visão executiva

O `gestor_os` é uma aplicação Django monolítica com módulos de:
- Cadastro (`cadastro`)
- Abertura de OS (`abertura_os`)
- Lançamento de horas (`lancamento_horas`)
- Relatórios (`relatorios`)
- Dashboard (`dashboard`)

A versão atual sobe em SQLite por padrão, suficiente para **desenvolvimento**. Para SaaS profissional, recomenda-se PostgreSQL, execução com Gunicorn e proxy reverso (Nginx), além de hardening de segurança.

---

## 2) Pré-requisitos

### Infra mínima (produção)
- Ubuntu 22.04+ (ou distro Linux equivalente)
- Python 3.12+
- `venv` e `pip`
- Nginx
- PostgreSQL 15+
- Systemd

### Dependências de sistema (renderização de PDF)
O projeto usa `weasyprint`, que pode exigir bibliotecas nativas.

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx postgresql postgresql-contrib \
  libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 \
  libffi-dev shared-mime-info
```

---

## 3) Estrutura recomendada de deploy

```text
/opt/gestor_os/
  ├── app/                 # código da aplicação
  ├── .venv/               # ambiente virtual
  ├── .env                 # variáveis sensíveis
  ├── logs/                # logs de aplicação
  └── run/                 # sockets/pids
```

---

## 4) Passo a passo — instalação base

## Passo 1: clonar o repositório
```bash
sudo mkdir -p /opt/gestor_os
sudo chown -R $USER:$USER /opt/gestor_os
cd /opt/gestor_os
git clone <URL_DO_REPOSITORIO> app
cd app
```

## Passo 2: criar ambiente virtual e instalar dependências
```bash
python3 -m venv /opt/gestor_os/.venv
source /opt/gestor_os/.venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

> Se houver erro de encoding no `requirements.txt`, converta para UTF-8 e reinstale:
```bash
python - <<'PY'
from pathlib import Path
p = Path('requirements.txt')
text = p.read_text(encoding='utf-16')
p.write_text(text, encoding='utf-8')
print('requirements.txt convertido para UTF-8')
PY
pip install -r requirements.txt
```

## Passo 3: validar o projeto
```bash
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## Passo 4: teste rápido local
```bash
python manage.py runserver 0.0.0.0:8000
```
Acesse: `http://SEU_IP:8000/login/`

---

## 5) Configuração SaaS (produção)

## Passo 5: banco PostgreSQL

```bash
sudo -u postgres psql
```
No prompt do PostgreSQL:
```sql
CREATE DATABASE gestor_os;
CREATE USER gestor_os_user WITH PASSWORD 'senha_forte_aqui';
GRANT ALL PRIVILEGES ON DATABASE gestor_os TO gestor_os_user;
\q
```

## Passo 6: externalizar configurações sensíveis

Crie `/opt/gestor_os/.env`:
```env
DJANGO_SECRET_KEY=troque_esta_chave
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=app.seudominio.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://app.seudominio.com
DATABASE_URL=postgresql://gestor_os_user:senha_forte_aqui@127.0.0.1:5432/gestor_os
```

> **Importante:** a base atual está com `SECRET_KEY` e `DEBUG` fixos em `settings.py`; em ambiente SaaS, adote leitura por variável de ambiente antes do go-live.

## Passo 7: Gunicorn (app server)

Instale Gunicorn:
```bash
source /opt/gestor_os/.venv/bin/activate
pip install gunicorn
```

Teste manual:
```bash
cd /opt/gestor_os/app
/opt/gestor_os/.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8001 --workers 3
```

Crie o serviço Systemd (`/etc/systemd/system/gestor_os.service`):
```ini
[Unit]
Description=Gestor OS - Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/gestor_os/app
Environment="PATH=/opt/gestor_os/.venv/bin"
ExecStart=/opt/gestor_os/.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8001 --workers 3 --timeout 120
Restart=always

[Install]
WantedBy=multi-user.target
```

Ative:
```bash
sudo systemctl daemon-reload
sudo systemctl enable gestor_os
sudo systemctl start gestor_os
sudo systemctl status gestor_os
```

## Passo 8: Nginx (proxy reverso + estáticos)

Arquivo `/etc/nginx/sites-available/gestor_os`:
```nginx
server {
    listen 80;
    server_name app.seudominio.com;

    client_max_body_size 20M;

    location /static/ {
        alias /opt/gestor_os/app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Ative site e recarregue:
```bash
sudo ln -s /etc/nginx/sites-available/gestor_os /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Passo 9: TLS (HTTPS)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d app.seudominio.com
```

---

## 6) Checklist de go-live 

- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` em variável de ambiente
- [ ] `ALLOWED_HOSTS` restrito ao domínio oficial
- [ ] PostgreSQL ativo com backup diário
- [ ] HTTPS obrigatório
- [ ] `collectstatic` executado a cada release
- [ ] Migrações aplicadas no deploy
- [ ] Superusuário de emergência com MFA no provedor de acesso
- [ ] Logs centralizados (Nginx + Systemd + app)
- [ ] Monitoramento (uptime, CPU, memória, erros 5xx)

---

## 7) Operação do dia a dia (runbook)

### Deploy de nova versão
```bash
cd /opt/gestor_os/app
git pull
source /opt/gestor_os/.venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gestor_os
sudo systemctl reload nginx
```

### Troubleshooting rápido
```bash
sudo journalctl -u gestor_os -n 200 --no-pager
sudo nginx -t
sudo systemctl status nginx gestor_os
python manage.py check
```

---

## 8) Ambientes recomendados

- **DEV:** SQLite + `runserver`
- **HML/STG:** PostgreSQL + Gunicorn + Nginx (espelhando produção)
- **PRD:** PostgreSQL gerenciado, backups automatizados, TLS, monitoramento e processo formal de release/rollback

---

## 9) KPIs de maturidade SaaS (sugestão)

- Disponibilidade mensal ≥ 99,5%
- MTTR (tempo de recuperação) < 30 min
- Taxa de erro 5xx < 0,5%
- Backup com teste de restauração mensal
- Janela de deploy com rollback validado

---

## 10) Próximos ganhos técnicos (roadmap)

1. Parametrizar `settings.py` via `.env` (segurança e portabilidade).
2. Adicionar CI com lint/test/migrations check.
3. Criar Dockerfile + docker-compose para padronização de ambientes.
4. Implementar observabilidade (Sentry + métricas Prometheus/Grafana).
5. Evoluir autenticação (MFA/SSO) para contexto corporativo.