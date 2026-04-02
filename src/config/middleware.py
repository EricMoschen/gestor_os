import time

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse

from .session_policy import (
    SESSION_LAST_ACTIVITY_KEY,
    SESSION_LOGIN_AT_KEY,
    SESSION_POLICY_KEY,
    TIMEOUT_REASON_ABSOLUTE,
    TIMEOUT_REASON_IDLE,
    get_session_config,
    resolve_session_policy,
)


class SessionTimeoutMiddleware:
    """Aplica timeout de sessão por inatividade e por duração máxima."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        login_url = reverse("login")
        logout_url = reverse("logout")

        if request.path in {login_url, logout_url}:
            return self.get_response(request)

        current_ts = int(time.time())

        policy = request.session.get(SESSION_POLICY_KEY) or resolve_session_policy(request.user)
        request.session[SESSION_POLICY_KEY] = policy
        config = get_session_config(policy)

        login_at = int(request.session.get(SESSION_LOGIN_AT_KEY, current_ts))
        last_activity = int(request.session.get(SESSION_LAST_ACTIVITY_KEY, current_ts))

        absolute_timeout_seconds = int(config["absolute_timeout_seconds"])
        if absolute_timeout_seconds and current_ts - login_at >= absolute_timeout_seconds:
            logout(request)
            return HttpResponseRedirect(f"{login_url}?timeout={TIMEOUT_REASON_ABSOLUTE}")

        uses_idle_timeout = bool(config["uses_idle_timeout"])
        idle_timeout_seconds = int(config["idle_timeout_seconds"])
        if uses_idle_timeout and current_ts - last_activity >= idle_timeout_seconds:
            logout(request)
            return HttpResponseRedirect(f"{login_url}?timeout={TIMEOUT_REASON_IDLE}")

        request.session[SESSION_LOGIN_AT_KEY] = login_at
        request.session[SESSION_LAST_ACTIVITY_KEY] = current_ts

        return self.get_response(request)