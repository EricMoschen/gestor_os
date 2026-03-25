from .base import * 
import dj_database_url
import os 

DEBUG = False

DATABASES={
    "default":dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    ) 
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "hhtps")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURA = True
CSRF_COOKIE_SECURE = True
