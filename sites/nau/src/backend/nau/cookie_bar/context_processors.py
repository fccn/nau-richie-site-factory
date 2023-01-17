"""
Cookie bar context processor
"""
from django.conf import settings


def cookie_bar_setting(request):
    """
    Cookie bar context processor
    """
    context = {}
    if hasattr(settings, "COOKIE_BAR"):
        context["COOKIE_BAR"] = getattr(settings, "COOKIE_BAR")
    return context
