from .session_policy import (
    SESSION_POLICY_DEFAULT,
    SESSION_POLICY_FABRICA,
    get_session_config,
)


def session_timeout_config(request):
    if not request.user.is_authenticated:
        return {}

    policy = request.session.get("session_policy", SESSION_POLICY_DEFAULT)
    if policy not in {SESSION_POLICY_DEFAULT, SESSION_POLICY_FABRICA}:
        policy = SESSION_POLICY_DEFAULT

    return {
        "session_timeout_config": {
            "policy": policy,
            **get_session_config(policy),
        }
    }