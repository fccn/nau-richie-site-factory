"""
Facebook pixel context processor
"""
from django.conf import settings


def facebook_pixel_setting(request):
    """
    Facebook Pixel context processor
    """
    context = {}
    if hasattr(settings, "FACEBOOK_PIXEL_ID"):
        context["FACEBOOK_PIXEL_ID"] = getattr(settings, "FACEBOOK_PIXEL_ID")
    return context
