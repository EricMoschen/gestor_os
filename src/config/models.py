from django.conf import settings
from django.db import models


class UserThemePreference(models.Model):
    THEME_DARK = "dark"
    THEME_LIGHT = "light"
    THEME_CHOICES = [ 
        (THEME_DARK, "Escuro"),
        (THEME_LIGHT, "Claro"),
    ] 

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="theme_preference",
    )
    theme = models.CharField(max_length=8, choices=THEME_CHOICES, default=THEME_DARK)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Preferência de tema"
        verbose_name_plural = "Preferências de tema"

    def __str__(self) -> str:
        return f"{self.user.username}: {self.theme}"