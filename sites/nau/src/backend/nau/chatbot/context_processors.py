"""
Chatbot widget context processor
"""
from django.conf import settings


def chatbot_widget_js_url_setting(request):
    """
    Chatbot widget context processor
    """
    context = {}
    if hasattr(settings, "CHATBOT_WIDGET_JS_URL"):
        context["CHATBOT_WIDGET_JS_URL"] = getattr(settings, "CHATBOT_WIDGET_JS_URL")
    return context
