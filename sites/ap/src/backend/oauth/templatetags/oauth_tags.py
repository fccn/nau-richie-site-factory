from django import template
from django.conf import settings

register = template.Library()


def validate_settings(auth_provider: str):
    for setting in [
        "SOCIAL_AUTH_{}_KEY",
        "SOCIAL_AUTH_{}_SECRET",
        "SOCIAL_AUTH_{}_AUTHORIZATION_URL",
        "SOCIAL_AUTH_{}_ACCESS_TOKEN_URL",
        "SOCIAL_AUTH_{}_USER_DATA_URL",
        "SOCIAL_AUTH_{}_SCOPE",
        "SOCIAL_AUTH_{}_REDIRECT_URI",
    ]:
        setting_value = getattr(settings, setting.format(auth_provider), None)
        if setting_value and setting_value.lstrip():
            return False

    return True


def validate_auth_backend(auth_provider: str):
    auth_backends = getattr(settings, "AUTHENTICATION_BACKENDS", ())
    if not auth_backends:
        return False

    for auth in auth_backends:
        if (
            f"{auth_provider}_oauth2_backend" in auth
            or f"social_core.backends.{auth_provider}" in auth
        ):
            return True

    return False


def get_validated_configs():
    oauth_configs = getattr(settings, "OAUTH_CONFIGS", [])
    valid_configs = []
    for config in oauth_configs:
        config_is_valid = validate_settings(config["backend"])
        config_is_valid = validate_auth_backend(config["backend"])

        if config_is_valid:
            valid_configs.append(config)

    return valid_configs


@register.simple_tag
def get_all_available_auth_providers():
    return get_validated_configs()
