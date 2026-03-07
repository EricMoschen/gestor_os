from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect

ROLE_ADM = "ADM"
ROLE_PCM = "PCM"
ROLE_SUPERVISOR = "Supervisor"
ROLE_ALMOXARIFE = "Almoxarife"

ALL_ROLES = [ROLE_ADM, ROLE_PCM, ROLE_SUPERVISOR, ROLE_ALMOXARIFE]

def ensure_roles_exist() -> None:
    for role in ALL_ROLES:
        Group.objects.get_or_create(name=role)


def user_has_any_role(user, allowed_roles: list[str]) -> bool:
    if not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    return user.groups.filter(name__in=allowed_roles).exists()


def role_required(allowed_roles: list[str]):
    def decoretor(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if user_has_any_role(request.user, allowed_roles):
                return view_func(request, *args, **kwargs)
            
            messages.error(request, "Você não tem permissão para acessar esta funcionalidade.")
            return redirect("dashboard")
        
        return _wrapped_view
    
    return decoretor
