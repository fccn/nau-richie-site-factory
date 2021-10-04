"""
Jira Service desk widget context processor
"""
from django.conf import settings


def jira_widget_key_setting(request):
    """
    Jira Service desk widget context processor
    """
    context = {}
    if hasattr(settings, "JIRA_WIDGET_KEY"):
        context["JIRA_WIDGET_KEY"] = getattr(settings, "JIRA_WIDGET_KEY")
    return context
