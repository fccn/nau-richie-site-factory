"""
Help Desk header url context processor
"""

from django.conf import settings


# pylint: disable=unused-argument
def help_desk_url_setting(request):
    """
    Help Desk header url context processor
    """
    context = {}
    if hasattr(settings, "HELP_DESK_URL"):
        context["HELP_DESK_URL"] = getattr(settings, "HELP_DESK_URL")
    return context
