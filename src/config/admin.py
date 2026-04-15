from django.contrib import admin

from .models import UserThemePreference


@admin.register(UserThemePreference)
class UserThemePreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "theme", "updated_at")
    search_fields = ("user__username",)
    list_filter = ("theme",)