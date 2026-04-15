from .models import UserThemePreference
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

def user_theme(request):
    default_theme = UserThemePreference.THEME_DARK

    if not request.user.is_authenticated:
        return {"active_theme": default_theme}
    
    preference = (
        UserThemePreference.objects
        .filter(user=request.user)
        .values_list("theme", flat=True)
        .first()
    )

    valid_choices = dict(UserThemePreference.THEME_CHOICES).keys()

    if preference not in valid_choices:
        preference = default_theme

    return {"active_theme": preference}