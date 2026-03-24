import os

DJANGO_ENV = os.getenv("DJANGO_ENV", "development").lower()

if DJANGO_ENV == "production":
    from .production import *  
elif DJANGO_ENV == "test":
    from .test import *  
else:
    from .development import *  