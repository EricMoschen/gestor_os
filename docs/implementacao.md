# Documentação de Implementação — Gestor OS

Este documento descreve como instalar, configurar, publicar e operar o projeto conforme o código atual.

---

## 1) Visão executiva

O `gestor_os` é uma aplicação Django monolítica organizada em apps de domínio:

- `config`: settings, autenticação, RBAC, sessão, tema e comando de superusuário;
- `dashboard`: tela inicial;
- `cadastro`: dados mestre;
- `abertura_os`: ciclo de vida da OS;
- `lancamento_horas`: apontamento e ajuste;
- `relatorios`: consolidação, logs e orçamentos.

Em desenvolvimento, a aplicação usa SQLite automaticamente quando `DATABASE_URL` não está configurada. Em produção, os settings esperam `DATABASE_URL` e forçam conexão com SSL.

---

## 2) Pré-requisitos

### Desenvolvimento

- Python compatível com Django 6.
- `venv` e `pip`.
- Dependências do `requirements.txt`.

### Produção Linux tradicional

- Python 3.12+ ou versão compatível com as dependências fixadas.
- Gunicorn.
- PostgreSQL ou outro banco exposto por `DATABASE_URL` compatível com `dj-database-url`.
- Nginx ou proxy equivalente.
- Bibliotecas nativas para renderização/documentos, especialmente se usar WeasyPrint.

Exemplo Ubuntu:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip nginx postgresql postgresql-contrib \
  libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 \
  libffi-dev shared-mime-info
```

---

## 3) Instalação local

```bash
git clone <URL_DO_REPOSITORIO> gestor_os
cd gestor_os
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/login/`.

> Se `requirements.txt` estiver salvo em UTF-16 no ambiente, converta para UTF-8 antes do `pip install`.

```bash
python - <<'PY'
from pathlib import Path
p = Path('requirements.txt')
text = p.read_text(encoding='utf-16')
p.write_text(text, encoding='utf-8')
print('requirements.txt convertido para UTF-8')
PY
```

---

## 4) Settings e variáveis de ambiente

O entrypoint (`manage.py`, `wsgi.py` e `asgi.py`) usa `DJANGO_SETTINGS_MODULE=src.config.settings`. Esse pacote escolhe o ambiente por `DJANGO_ENV`:

| `DJANGO_ENV` | Arquivo carregado | Comportamento |
| --- | --- | --- |
| ausente ou `development` | `src.config.settings.development` | `DEBUG=True`, `ALLOWED_HOSTS=["*"]`, SQLite se não houver `DATABASE_URL`. |
| `production` | `src.config.settings.production` | `DEBUG=False`, banco por `DATABASE_URL`, SSL redirect e cookies seguros. |
| `test` | `src.config.settings.test` | `DEBUG=False`, hasher MD5 para testes. |

Variáveis recomendadas em produção:

```env
DJANGO_ENV=production
DJANGO_SECRET_KEY=troque_esta_chave
DJANGO_ALLOWED_HOSTS=app.seudominio.com
DATABASE_URL=postgresql://usuario:senha@host:5432/gestor_os
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=senha_forte
DJANGO_SUPERUSER_EMAIL=admin@seudominio.com
```

Observações:

- `SECRET_KEY` também é aceito como fallback de `DJANGO_SECRET_KEY`.
- `CSRF_TRUSTED_ORIGINS` está definido no código para localhost e o domínio Render atual; adicione novos domínios no settings antes do go-live se necessário.
- `SESSION_IDLE_TIMEOUT_MINUTES=10` e `SESSION_FABRICA_ABSOLUTE_TIMEOUT_HOURS=12` estão definidos no settings base.

---

## 5) Banco de dados

### Desenvolvimento

Sem `DATABASE_URL`, o banco padrão é `src/db.sqlite3`.

```bash
python manage.py migrate
```

### Produção com PostgreSQL

Exemplo de criação local:

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE gestor_os;
CREATE USER gestor_os_user WITH PASSWORD 'senha_forte_aqui';
GRANT ALL PRIVILEGES ON DATABASE gestor_os TO gestor_os_user;
\q
```

Configure:

```env
DATABASE_URL=postgresql://gestor_os_user:senha_forte_aqui@127.0.0.1:5432/gestor_os
```

---

## 6) Comando de superusuário automatizado

O projeto inclui:

```bash
python manage.py ensure_superuser
```

Ele lê:

- `DJANGO_SUPERUSER_USERNAME`;
- `DJANGO_SUPERUSER_PASSWORD`;
- `DJANGO_SUPERUSER_EMAIL`.

Em `DJANGO_ENV=production`, a falta de usuário/senha ou senha inválida interrompe o comando com erro. Nos demais ambientes, apenas emite aviso.

---

## 7) Deploy em Render

O arquivo `render.yaml` atual define:

- serviço web Python chamado `gestor-os`;
- build com instalação de dependências, migrações, `collectstatic` e `ensure_superuser`;
- start com Gunicorn;
- variáveis `DJANGO_ENV=production`, `SECRET_KEY`, `DATABASE_URL` e credenciais de superusuário.

Atenção: os entrypoints Python do projeto usam o módulo `src.config.settings` e a aplicação WSGI `src.config.wsgi:application`. Se o provedor não ajustar `PYTHONPATH` automaticamente para `src`, prefira comandos explícitos:

```yaml
startCommand: "gunicorn src.config.wsgi:application --bind 0.0.0.0:$PORT"
envVars:
  - key: DJANGO_SETTINGS_MODULE
    value: src.config.settings
```

---

## 8) Deploy Linux com Gunicorn + Nginx

### Gunicorn manual

```bash
source /opt/gestor_os/.venv/bin/activate
cd /opt/gestor_os/app
gunicorn src.config.wsgi:application --bind 127.0.0.1:8001 --workers 3 --timeout 120
```

### Serviço Systemd

`/etc/systemd/system/gestor_os.service`:

```ini
[Unit]
Description=Gestor OS - Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/gestor_os/app
Environment="PATH=/opt/gestor_os/.venv/bin"
Environment="DJANGO_ENV=production"
EnvironmentFile=/opt/gestor_os/app/.env
ExecStart=/opt/gestor_os/.venv/bin/gunicorn src.config.wsgi:application --bind 127.0.0.1:8001 --workers 3 --timeout 120
Restart=always

[Install]
WantedBy=multi-user.target
```

Ativação:

```bash
sudo systemctl daemon-reload
sudo systemctl enable gestor_os
sudo systemctl start gestor_os
sudo systemctl status gestor_os
```

### Nginx

```nginx
server {
    listen 80;
    server_name app.seudominio.com;

    client_max_body_size 20M;

    location /static/ {
        alias /opt/gestor_os/app/src/staticfiles/;
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

> `STATIC_ROOT` é calculado a partir de `BASE_DIR`, que aponta para `src`; portanto, o destino atual do `collectstatic` é `src/staticfiles`.

---

## 9) Checklist de release

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py ensure_superuser
```

Validações manuais mínimas:

- login e logout;
- dashboard por perfil;
- criação de OS;
- apontamento de horas;
- finalização de OS;
- relatório/orçamento;
- troca de tema, se alterada interface global.

---

## 10) Runbook de atualização

```bash
cd /opt/gestor_os/app
git pull
source /opt/gestor_os/.venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py ensure_superuser
sudo systemctl restart gestor_os
sudo systemctl reload nginx
```

Troubleshooting:

```bash
sudo journalctl -u gestor_os -n 200 --no-pager
sudo nginx -t
python manage.py check
python manage.py showmigrations
```

---

## 11) Checklist de go-live

- [ ] `DJANGO_ENV=production`.
- [ ] `DJANGO_SECRET_KEY`/`SECRET_KEY` definido fora do código.
- [ ] `DJANGO_ALLOWED_HOSTS` restrito.
- [ ] `DATABASE_URL` configurado com backup.
- [ ] HTTPS ativo.
- [ ] `collectstatic` executado.
- [ ] Migrações aplicadas.
- [ ] `ensure_superuser` validado.
- [ ] Permissões dos grupos revisadas.
- [ ] Logs e monitoramento configurados.
