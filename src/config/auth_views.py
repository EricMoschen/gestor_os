import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .access_control import ensure_roles_exist
from .session_policy import (
    SESSION_LAST_ACTIVITY_KEY,
    SESSION_LOGIN_AT_KEY,
    SESSION_POLICY_KEY,
    TIMEOUT_REASON_ABSOLUTE,
    TIMEOUT_REASON_IDLE,
    resolve_session_policy,
)


def _get_timeout_error_message(timeout_reason: str | None) -> str | None:
    if timeout_reason == TIMEOUT_REASON_IDLE:
        return "Sua sessão expirou por inatividade. Faça login novamente."

    if timeout_reason == TIMEOUT_REASON_ABSOLUTE:
        return "Sua sessão expirou após o período máximo permitido. Faça login novamente."

    return None


def login_view(request):
    ensure_roles_exist()

    if request.user.is_authenticated:
        return redirect("dashboard")

    timeout_reason = request.GET.get("timeout")
    error_message = _get_timeout_error_message(timeout_reason)

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            now_ts = int(time.time())
            request.session[SESSION_POLICY_KEY] = resolve_session_policy(user)
            request.session[SESSION_LOGIN_AT_KEY] = now_ts
            request.session[SESSION_LAST_ACTIVITY_KEY] = now_ts

            return redirect("dashboard")

        error_message = "Usuário ou senha inválidos."

    return render(request, "auth/login.html", {"error_message": error_message})


@login_required
def logout_view(request):
    timeout_reason = request.GET.get("timeout")
    logout(request)

    if timeout_reason in {TIMEOUT_REASON_IDLE, TIMEOUT_REASON_ABSOLUTE}:
        return redirect(f"{reverse('login')}?timeout={timeout_reason}")

    return redirect("login")