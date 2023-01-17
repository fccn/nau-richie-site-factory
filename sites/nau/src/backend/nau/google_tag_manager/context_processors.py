"""
Google Tag Manager widget context processor
"""
from django.conf import settings


def google_tag_manager_setting(request):
    """
    Google Tag Manager widget context processor
    """
    context = {}
    if hasattr(settings, "GOOGLE_TAG_MANAGER_ID"):
        context["GOOGLE_TAG_MANAGER_ID"] = getattr(settings, "GOOGLE_TAG_MANAGER_ID")
    if hasattr(settings, "GOOGLE_TAG_MANAGER_ENVIRONMENT"):
        context["GOOGLE_TAG_MANAGER_ENVIRONMENT"] = getattr(
            settings, "GOOGLE_TAG_MANAGER_ENVIRONMENT"
        )
    return context
