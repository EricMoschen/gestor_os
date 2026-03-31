from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

# Register your models here.

app_config = apps.get_app_config("abertura_os")

for model in app_config.get_models():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass