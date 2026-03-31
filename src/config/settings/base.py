from pathlib import Path
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parents[2]

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    os.getenv(
        "SECRET_KEY",
    "django-insecure-ew@5e7badi5^wq#)bzyrz!j%ea9rx*+9@2a8z(^7_+fd1@f2b7",
    ),
)


DEBUG = False


allowed_hosts_env = os.getenv("DJANGO_ALLOWED_HOSTS", "gestor-os-90c6.onrender.com")
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(",") if host.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "src.cadastro",
    "src.abertura_os",
    "src.lancamento_horas",
    "src.relatorios",
    "src.dashboard",
    "src.config",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "src.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "src.config.wsgi.application"
ASGI_APPLICATION = "src.config.asgi.application"

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "https://localhost:8001",
    "https://localhost:8000",
    "http://127.0.0.1:8000",
    "https://127.0.0.1:8000",
    "https://localhost:8080",
    "http://127.0.0.1:8080",
    "https://gestor-os-90c6.onrender.com",
]

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"