import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "Garante a criação de um superusuário a partir de variáveis de ambiente."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Superusuário não criado: defina DJANGO_SUPERUSER_USERNAME e DJANGO_SUPERUSER_PASSWORD."
                )
            )
            return

        user_model = get_user_model()

        if user_model.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superusuário '{username}' já existe. Nenhuma ação necessária."
                )
            )
            return

        try:
            validate_password(password)
        except ValidationError as exc:
            raise CommandError(
                "Senha de superusuário inválida: " + "; ".join(exc.messages)
            ) from exc

        user_model.objects.create_superuser(
            username=username,
            password=password,
            email=email,
        )
        self.stdout.write(self.style.SUCCESS(f"Superusuário '{username}' criado com sucesso."))
