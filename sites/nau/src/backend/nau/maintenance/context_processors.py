"""
Jira Service desk widget context processor
"""
from django.conf import settings


def maintenance_header_message_setting(request):
    """
    Maintenance header message
    """
    context = {}
    if hasattr(settings, "MAINTENANCE_HEADER_MSG"):
        context["MAINTENANCE_HEADER_MSG"] = getattr(settings, "MAINTENANCE_HEADER_MSG")
    return context
