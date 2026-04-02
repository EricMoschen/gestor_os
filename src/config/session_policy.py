from datetime import timedelta

from .access_control import ROLE_FABRICA

# Políticas de sessão (em segundos)
DEFAULT_IDLE_TIMEOUT_SECONDS = 10 * 60
DEFAULT_WARNING_THRESHOLD_SECONDS = 2 * 60
FABRICA_ABSOLUTE_TIMEOUT_SECONDS = int(timedelta(hours=8).total_seconds())

SESSION_POLICY_DEFAULT = "default"
SESSION_POLICY_FABRICA = "fabrica"

SESSION_POLICY_KEY = "session_policy"
SESSION_LAST_ACTIVITY_KEY = "last_activity_ts"
SESSION_LOGIN_AT_KEY = "login_at_ts"
TIMEOUT_REASON_IDLE = "idle"
TIMEOUT_REASON_ABSOLUTE = "absolute"


def resolve_session_policy(user) -> str:
    if user.groups.filter(name=ROLE_FABRICA).exists():
        return SESSION_POLICY_FABRICA

    return SESSION_POLICY_DEFAULT


def get_session_config(policy: str) -> dict[str, int | bool]:
    if policy == SESSION_POLICY_FABRICA:
        return {
            "uses_idle_timeout": False,
            "idle_timeout_seconds": DEFAULT_IDLE_TIMEOUT_SECONDS,
            "warning_threshold_seconds": 0,
            "absolute_timeout_seconds": FABRICA_ABSOLUTE_TIMEOUT_SECONDS,
        }

    return {
        "uses_idle_timeout": True,
        "idle_timeout_seconds": DEFAULT_IDLE_TIMEOUT_SECONDS,
        "warning_threshold_seconds": DEFAULT_WARNING_THRESHOLD_SECONDS,
        "absolute_timeout_seconds": 0,
    }