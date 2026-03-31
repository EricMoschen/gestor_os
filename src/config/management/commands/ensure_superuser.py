import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Cria ou atualiza o superusuário a partir das variáveis de ambiente."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        django_env = os.getenv("DJANGO_ENV", "").strip().lower()

        if not username or not password:
            message = (
                "Superusuário não criado: defina DJANGO_SUPERUSER_USERNAME e "
                "DJANGO_SUPERUSER_PASSWORD."
            )
            if django_env == "production":
                raise CommandError(message)

            self.stdout.write(self.style.WARNING(message))
            return

        user_model = get_user_model()

        try:
            validate_password(password)
        except ValidationError as exc:
            message = "Senha de superusuário inválida (" + "; ".join(exc.messages) + ")."
            if django_env == "production":
                raise CommandError(message) from exc

            self.stdout.write(self.style.WARNING(message))
            return

        user, created = user_model.objects.get_or_create(username=username, defaults={
            "email": email,
        })

        # Atualiza senha e email mesmo se já existir
        user.set_password(password)
        user.email = email
        user.is_superuser = True
        user.is_staff = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superusuário '{username}' criado com sucesso."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superusuário '{username}' já existia, senha e email atualizados."))